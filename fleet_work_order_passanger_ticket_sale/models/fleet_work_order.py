# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class FleetWorkOrder(models.Model):
    _inherit = ["fleet.work.order"]

    @api.multi
    def button_buy_ticket(self):
        self.ensure_one()
        waction = self.env.ref(
            "fleet_work_order_passanger_ticket_sale."
            "fleet_work_order_passanger_ticket_sale_simple_action").read()[0]
        waction.update({
            "context": {"default_work_order_id": self.id},
            "res_id": False,
        })
        return waction
