# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp.tests.common import TransactionCase


class TestWorkOrder(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super(TestWorkOrder, self).setUp(*args, **kwargs)
        self.driver = self.env.ref("fleet_work_order.driver1")
        self.vehicle = self.env.ref("fleet.vehicle_1")
        self.wo_type = self.env.ref("fleet_work_order.type_3")
        self.obj_depart = self.env["fleet.work.order.depart"]
        self.obj_arrive = self.env["fleet.work.order.arrive"]
        self.obj_wo_type = self.env["fleet.work.order.type"]
        self.obj_wo_type_route = self.env["fleet.work.order.type.route"]
        self.point1 = self.env.ref("fleet_work_order.point1")
        self.point2 = self.env.ref("fleet_work_order.point2")
        self.point3 = self.env.ref("fleet_work_order.point3")
        self.point4 = self.env.ref("fleet_work_order.point4")
        self.route_template_1 = self.env.ref(
            "fleet_work_order_multiple_route.route_template_2"
        )

        res = {
            "date_start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date_end": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.order = self.env["fleet.work.order"].create(res)

        return result

    def test_1(self):
        res = {
            "name": "Test Route",
            "multiple_route": True,
            "start_location_id": self.point3.id,
            "end_location_id": self.point4.id,
            "code": "-",
        }
        wo_type = self.obj_wo_type.create(res)
        res1 = {
            "type_id": wo_type.id,
            "name": "Test WO Type Route 1",
            "start_location_id": self.point1.id,
            "end_location_id": self.point2.id,
            "distance": 30.0,
        }
        route1 = self.obj_wo_type_route.create(res1)
        self.assertEqual(
            wo_type.function_start_location_id.id,
            self.point1.id,
        )
        self.assertEqual(
            wo_type.function_end_location_id.id,
            self.point2.id,
        )
        wo_type.multiple_route = False
        self.assertEqual(
            wo_type.function_start_location_id.id,
            self.point3.id,
        )
        self.assertEqual(
            wo_type.function_end_location_id.id,
            self.point4.id,
        )
        route1.route_template_id = self.route_template_1.id
        route1.onchange_route_template()
        self.assertEqual(
            route1.start_location_id.id,
            self.point4.id,
        )
        self.assertEqual(
            route1.end_location_id.id,
            self.point3.id,
        )

    def test_2(self):
        res = {
            "name": "Test Route",
            "multiple_route": True,
            "start_location_id": self.point3.id,
            "end_location_id": self.point4.id,
            "code": "-",
        }
        wo_type_1 = self.obj_wo_type.create(res)
        self.order.type_id = wo_type_1.id
        self.order.onchange_type_id()
        self.assertEqual(self.order.function_start_location_id.id, self.point3.id)
        self.assertEqual(self.order.function_end_location_id.id, self.point4.id)
        wo_type_2 = wo_type_1.copy()
        res1 = {
            "type_id": wo_type_2.id,
            "name": "Test WO Type Route 1",
            "start_location_id": self.point1.id,
            "end_location_id": self.point2.id,
            "distance": 30.0,
        }
        self.obj_wo_type_route.create(res1)
        self.order.type_id = wo_type_2.id
        self.order.onchange_type_id()
        wo_route = self.order.route_ids[0]
        wo_route.route_template_id = self.route_template_1.id
        wo_route.onchange_route_template_id()
