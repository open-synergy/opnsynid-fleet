# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class TestFleetWorkOrder(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestFleetWorkOrder, self).setUp(*args, **kwargs)

        self.obj_picking = self.env["stock.picking"]
        self.obj_wizard = self.env["shipment.plan.creator"]
        self.obj_procurement = self.env["procurement.order"]
        self.obj_wo = self.env["fleet.work.order"]
        self.obj_depart = self.env["fleet.work.order.depart"]
        self.obj_arrive = self.env["fleet.work.order.arrive"]

        self.warehouse = self.env.ref(
            "stock.warehouse0")
        self.partner1 = self.env.ref(
            "base.res_partner_19")
        self.warehouse.write({
            "delivery_steps": "ship_transit",
        })
        self.transit_loc = self.warehouse.wh_transit_out_loc_id
        self.do_type = self.warehouse.out_type_id
        self.cr_type = self.warehouse.transit_out_type_id
        self.loc = self.cr_type.default_location_src_id
        self.dest_loc = self.cr_type.default_location_dest_id
        self.product1 = self.env.ref("product.product_product_5b")
        self.driver = self.env.ref("fleet_work_order.driver1")
        self.vehicle = self.env.ref("fleet.vehicle_1")
        criteria = [
            ("location_id", "=",  self.cr_type.default_location_dest_id.id),
            ("location_src_id", "=", self.cr_type.default_location_src_id.id),
            ("warehouse_id", "=", self.warehouse.id),
            ]
        self.rule = self.env[
            "procurement.rule"].search(
                criteria, limit=1)

    def _create_customer_reception(self):
        res = {
            "partner_id": self.partner1.id,
            "origin_address_id": self.warehouse.partner_id.id,
            "delivery_address_id": self.partner1.id,
            "picking_type_id": self.cr_type.id,
            "move_lines": [
                (0, 0, {
                    "name": self.product1.name,
                    "product_id": self.product1.id,
                    "product_uom_qty": 3.0,
                    "product_uom": self.product1.uom_id.id,
                    "location_id": self.loc.id,
                    "location_dest_id": self.dest_loc.id,
                    "procure_method": "make_to_order",
                })],
        }
        picking = self.obj_picking.create(res)
        return picking

    def _create_work_order(self, cargos=False):
        data = {
            "vehicle_id": self.vehicle.id,
            "driver_id": self.driver.id,
            "date_start": "2016-01-01 00:00:00",
            "date_end": "2016-01-02 00:00:00",
            "cargo_ids": [],
        }
        self.assertEqual(
            len(cargos),
            1)
        if cargos:
            data["cargo_ids"].append((6, 0, cargos.ids))

        wo = self.obj_wo.create(data)
        return wo

    def _confirm_no_error(self, order):
        order.button_confirm()
        self.assertEqual(order.state, "confirmed")

    def _depart_no_error(self, order):
        context = {
            "active_ids": [order.id],
        }
        wzd_depart = self.obj_depart.with_context(context).create({
            "date_depart": order.date_start,
            "start_odometer": 0
        })
        wzd_depart.button_depart()
        self.assertEqual(order.state, "depart")
        self.assertNotEqual(order.name, "/")

    def _depart_error_cargo_not_ready(self, order):
        context = {
            "active_ids": [order.id],
        }
        wzd_depart = self.obj_depart.with_context(context).create({
            "date_depart": order.date_start,
            "start_odometer": 0
        })
        with self.assertRaises(ValidationError):
            wzd_depart.button_depart()


    def _arrive_error(self, order):
        wzd_arrive = self.obj_arrive.create({
            "date_arrive": order.date_end,
            "end_odometer": order.distance,
        })

        with self.assertRaises(ValidationError):
            wzd_arrive.with_context({
                "active_ids": [order.id],
            }).button_arrive()

    def _arrive_no_error(self, order):
        wzd_arrive = self.obj_arrive.create({
            "date_arrive": order.date_end,
            "end_odometer": order.distance,
        })

        wzd_arrive.with_context({
            "active_ids": [order.id],
        }).button_arrive()
        self.assertEqual(order.state, "arrive")

    def _process_procurement(self, picking):
        move1 = picking.move_lines[0]
        criteria = [
            ("move_dest_id", "=", move1.id)]
        procurement = self.obj_procurement.search(
            criteria, limit=1)[0]
        procurement.write({
            "rule_id": self.rule.id})
        procurement.run()
        procurement.check()
        self.assertEqual(
            procurement.state,
            "running")
        move2 = procurement.move_ids[0]
        do = move2.picking_id
        return do

    def _create_shipments(self, moves):
        context = {
            "active_model": "stock.move",
            "active_ids": moves.ids,
        }

        wizard = self.obj_wizard.with_context(context).create({
            "from_address_id": self.warehouse.partner_id.id,
            "to_address_id": self.partner1.id})
        wizard.action_create_shipment()
        return moves[0].departure_shipment_id

    def test_fleet_work_order_cargo_not_ready(self):
        cr = self._create_customer_reception()
        cr.action_confirm()
        do = self._process_procurement(cr)
        shipment = self._create_shipments(do.move_lines[0])
        wo = self._create_work_order(shipment)
        self._confirm_no_error(wo)
        self._depart_error_cargo_not_ready(wo)

    def test_fleet_work_order_cargo_not_done(self):
        cr = self._create_customer_reception()
        cr.action_confirm()
        do = self._process_procurement(cr)
        shipment = self._create_shipments(do.move_lines[0])
        wo = self._create_work_order(shipment)
        do.action_confirm()
        do.force_assign()
        do.action_done()
        self._confirm_no_error(wo)
        shipment.signal_workflow("shipment_confirm")
        shipment.button_action_transit()
        self._depart_no_error(wo)
        self._arrive_error(wo)

    def test_fleet_work_order_cargo_no_error(self):
        cr = self._create_customer_reception()
        cr.action_confirm()
        do = self._process_procurement(cr)
        shipment = self._create_shipments(do.move_lines[0])
        wo = self._create_work_order(shipment)
        do.action_confirm()
        do.force_assign()
        do.action_done()
        self._confirm_no_error(wo)
        shipment.signal_workflow("shipment_confirm")
        shipment.button_action_transit()
        self._depart_no_error(wo)
        cr.force_assign()
        cr.action_done()
        self._arrive_no_error(wo)
