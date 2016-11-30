# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestFleetSchedule(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestFleetSchedule, self).setUp(*args, **kwargs)

        self.type3 = self.env.ref(
            "fleet_work_order.type_3")

    def test_schedule(self):
        obj_schedule = self.env[
            "fleet.work.order.type.schedule"]
        obj_order = self.env[
            "fleet.work.order"]
        self.type3.action_add_schedule()

        self.assertEqual(
            len(self.type3.schedule_ids),
            1)

        before = obj_order.search_count(
            [("type_id", "=", self.type3.id)])

        obj_schedule.run_schedule(
            self.type3.schedule_ids[0].id)

        after = obj_order.search_count(
            [("type_id", "=", self.type3.id)])

        self.assertEqual(
            after,
            before + 1)

        self.type3.schedule_ids[0].unlink()
