# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class WorkOrderTypeRoute(models.Model):
    _inherit = "fleet.work.order.type.route"

    gamification_point = fields.Float(
        string="Gamification Point",
        default=1.0
    )

    @api.multi
    @api.onchange(
        "route_template_id"
    )
    def onchange_gamification_point(self):
        if not self.route_template_id:
            self.gamification_point = 1.0
            return
        self.gamification_point =\
            self.route_template_id.gamification_point
