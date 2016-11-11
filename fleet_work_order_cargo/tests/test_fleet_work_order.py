# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


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
        self.product1 = self.env.ref("product.product_product_5b")
        self.driver = self.env.ref("fleet_work_order.driver1")
        self.vehicle = self.env.ref("fleet.vehicle_1")
        self.rule = self.env[
            "procurement.rule"].search(
                [
                    ("location_id", "=",  self.cr_type.default_location_dest_id.id),
                    ("location_src_id", "=", self.cr_type.default_location_src_id.id),
                    ("warehouse_id", "=", self.warehouse.id),
                    ], limit=1)

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
                    "location_id": self.cr_type.default_location_src_id.id,
                    "location_dest_id": self.cr_type.default_location_dest_id.id,
                    "procure_method": "make_to_order",
                    })],
                }
        picking = self.obj_picking.create(res)
        return picking

    def _create_work_order(self, cargos=False):
        data = {
            "vehicle_id": self.vehicle.id,
            "date_start": "2016-01-01 00:00:00",
            "date_end": "2016-01-02 00:00:00",
            "cargo_ids": [],
        }
        if cargos:
            data["cargo_ids"].append(6, 0, cargos.ids)

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

    def test_fleet_work_order(self):
        cr = self._create_customer_reception()
        cr.action_confirm()
        move1 = cr.move_lines[0]
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

        context = {
            "active_model": "stock.move",
            "active_ids": [move2.id],
            }

        self.obj_wizard.with_context(context).create({})
        shipment = move2.departure_shipment_id
        wo = self._create_work_order(shipment)
        self._confirm_no_error(wo)
        self._depart_no_error(wo)
