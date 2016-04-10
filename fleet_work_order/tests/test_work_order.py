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

        self.passanger_1 = self.env.ref("base.res_partner_address_2")
        self.passanger_2 = self.env.ref("base.res_partner_address_1")
        self.passanger_3 = self.env.ref("base.res_partner_address_7")

        return result

    def _prepare_work_order_data(self):
        data = {
            "vehicle_id": self.vehicle.id,
            "driver_id": self.driver.id,
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
        data = self._prepare_work_order_data()
        data.update({"passanger_manifest": True, "passanger_count": 3})
        order = self._create_no_error(data)
        self._confirm_no_error(order)
        self._depart_error(order)

        return order

    def test_create_8(self):
        data = self._prepare_work_order_data()
        data_addition = {
            "passanger_manifest": True,
            "passanger_count": 3,
        }
        data.update(data_addition)
        order = self._create_no_error(data)
        self._confirm_no_error(order)

        manifest_1 = self._register_passanger(order, self.passanger_1)
        manifest_2 = self._register_passanger(order, self.passanger_2)
        manifest_3 = self._register_passanger(order, self.passanger_3)

        self._confirm_passanger(manifest_1)
        self._confirm_passanger(manifest_2)
        self._confirm_passanger(manifest_3)

        self._boarding_passanger(manifest_1)
        self._boarding_passanger(manifest_2)
        self._boarding_passanger(manifest_3)

        self._depart_no_error(order)
        self._arrive_no_error(order)

        return order

    def _create_no_error(self, data):
        order_obj = self.env["fleet.work.order"]
        order = order_obj.create(data)
        self.assertIsNotNone(order)
        self.assertEqual(order.state, "draft")

        return order

    def _confirm_no_error(self, order):
        order.button_confirm()
        self.assertEqual(order.state, "confirmed")

    def _depart_no_error(self, order):
        order.button_depart()
        self.assertEqual(order.state, "depart")
        self.assertNotEqual(order.name, "/")

    def _depart_error(self, order):
        with self.assertRaises(except_orm):
            order.button_depart()

    def _arrive_no_error(self, order):
        order.button_arrive()
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

    def _register_passanger(self, order, passanger):
        passanger_obj = self.env['fleet.passanger.manifest']
        data = {
            "order_id": order.id,
            "partner_id": passanger.id,
        }
        passanger = passanger_obj.create(data)
        self.assertEqual(passanger.state, "draft")
        self.assertEqual(passanger.name, "/")
        return passanger

    def _confirm_passanger(self, passanger):
        passanger.button_confirm()
        self.assertEqual(passanger.state, "confirmed")
        self.assertNotEqual(passanger.name, "/")

    def _boarding_passanger(self, passanger):
        passanger.button_boarding()
        self.assertEqual(passanger.state, "boarding")
