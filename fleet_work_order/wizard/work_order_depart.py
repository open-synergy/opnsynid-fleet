# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


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
        self._depart(self)

    @api.model
    def _depart(self, wizard):
        order_ids = self.env.context["active_ids"]
        order = self.env["fleet.work.order"].browse(order_ids)

        order._action_depart(order, 
            date_depart=wizard.date_depart,
            starting_odometer=wizard.start_odometer,
            )
