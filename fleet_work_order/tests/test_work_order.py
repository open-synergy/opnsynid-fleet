# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import except_orm


class TestWorkOrder(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super(TestWorkOrder, self).setUp(*args, **kwargs)
        self.driver = self.env.ref("fleet_work_order.driver1")
        self.vehicle = self.env.ref("fleet.vehicle_1")
        self.wo_type = self.env.ref("fleet_work_order.type_3")
        self.obj_depart = self.env["fleet.work.order.depart"]
        self.obj_arrive = self.env["fleet.work.order.arrive"]

        return result

    def _prepare_work_order_data(self):
        data = {
            "vehicle_id": self.vehicle.id,
            "date_start": "2016-01-01 00:00:00",
            "date_end": "2016-01-02 00:00:00",
        }
        return data

    def _prepare_work_order_data_2(self):
        data = {
            "type_id": self.wo_type.id,
            "date_start": "2016-01-01 00:00:00",
            "date_end": "2016-01-02 00:00:00",
        }

        return data

    def test_create_1(self):
        data = self._prepare_work_order_data()
        order = self._create_no_error(data)
        self._confirm_no_error(order)
        self._depart_no_error(order)
        self._arrive_no_error(order)
        self._cancel_no_error(order)
        self._restart_number_assign(order)

        return order

    def test_create_2(self):
        data = self._prepare_work_order_data()
        order = self._create_no_error(data)
        self._cancel_no_error(order)
        self._restart_number_no_assign(order)

        return order

    def test_create_3(self):
        data = self._prepare_work_order_data()
        order = self._create_no_error(data)
        self._confirm_no_error(order)
        self._cancel_no_error(order)
        self._restart_number_assign(order)

        return order

    def test_create_4(self):
        data = self._prepare_work_order_data()
        order = self._create_no_error(data)
        self._confirm_no_error(order)
        self._depart_no_error(order)
        self._cancel_no_error(order)
        self._restart_number_assign(order)

        return order

    def test_create_5(self):
        data = self._prepare_work_order_data_2()
        order = self._create_no_error_2(data)
        self._confirm_no_error(order)
        self._depart_no_error(order)
        self._arrive_no_error(order)
        self._cancel_no_error(order)
        self._restart_number_assign(order)

        return order

    def _create_no_error(self, data):
        order_obj = self.env["fleet.work.order"]
        order = order_obj.create(data)
        order.onchange_vehicle_id()
        self.assertIsNotNone(order)
        self.assertEqual(order.state, "draft")
        self.assertEqual(
            order.driver_id,
            order.vehicle_id.driver_id)

        return order

    def _create_no_error_2(self, data):
        order_obj = self.env["fleet.work.order"]
        order = order_obj.create(data)
        order.onchange_type_id()
        self.assertIsNotNone(order)
        self.assertEqual(order.state, "draft")
        self.assertEqual(
            order.start_location_id,
            order.type_id.start_location_id)
        self.assertEqual(
            order.end_location_id,
            order.type_id.end_location_id)
        self.assertEqual(
            order.distance,
            order.type_id.distance)
        self.assertEqual(
            order.vehicle_id,
            order.type_id.vehicle_id)
        self.assertEqual(
            order.driver_id,
            order.type_id.driver_id)
        self.assertEqual(
            order.co_driver_id,
            order.type_id.co_driver_id)

        return order

    def _confirm_no_error(self, order):
        order.button_confirm()
        self.assertEqual(order.state, "confirmed")

    def _depart_no_error(self, order):
        wzd_depart = self.obj_depart.create({
            "date_depart": order.date_start,
            "start_odometer": 0
        })

        wzd_depart.with_context({
            "active_ids": [order.id],
        }).button_depart()
        self.assertEqual(order.state, "depart")
        self.assertNotEqual(order.name, "/")

    def _depart_error(self, order):
        with self.assertRaises(except_orm):
            order.button_depart()

    def _arrive_no_error(self, order):
        wzd_arrive = self.obj_arrive.create({
            "date_arrive": order.date_end,
            "end_odometer": order.distance,
        })

        wzd_arrive.with_context({
            "active_ids": [order.id],
        }).button_arrive()
        self.assertEqual(order.state, "arrive")

    def _cancel_no_error(self, order):
        order.button_cancel()
        self.assertEqual(order.state, "cancelled")

    def _restart_number_assign(self, order):
        order.button_restart()
        self.assertEqual(order.state, "draft")
        self.assertNotEqual(order.name, "/")

    def _restart_number_no_assign(self, order):
        order.button_restart()
        self.assertEqual(order.state, "draft")
        self.assertEqual(order.name, "/")
