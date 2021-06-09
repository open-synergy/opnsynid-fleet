# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.exceptions import Warning as UserError

from .base import BaseFleetWorkOrderRouteDistance


class TestCalcDistance(BaseFleetWorkOrderRouteDistance):
    def _create_work_order(self):
        data = {
            "date_start": "2016-01-01 00:00:00",
            "date_end": "2016-01-02 00:00:00",
        }
        order = self.order_obj.create(data)

        return order

    def test_calc_distance(self):
        order = self._create_work_order()

        msg = "Start Location and End Location can't be empty"

        with self.assertRaises(UserError) as error:
            order.button_calc_distance()
        self.assertEqual(error.exception.message, msg)
