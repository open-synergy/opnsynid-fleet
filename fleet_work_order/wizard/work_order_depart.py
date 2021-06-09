# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class WorkOrderDepart(models.TransientModel):
    _name = "fleet.work.order.depart"
    _description = "Work Order Arrive"

    date_depart = fields.Datetime(
        string="Date Depart",
        required=True,
        default=fields.Datetime.now(),
    )
    start_odometer = fields.Float(
        string="Starting Odometer",
        required=True,
    )

    @api.multi
    def button_depart(self):
        self.ensure_one()
        self._depart()

    @api.multi
    def _depart(self):
        order_ids = self.env.context["active_ids"]
        order = self.env["fleet.work.order"].browse(order_ids)

        order._action_depart(
            date_depart=self.date_depart,
            starting_odometer=self.start_odometer,
        )
