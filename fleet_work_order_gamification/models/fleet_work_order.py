# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    gamification_point = fields.Float(string="Gamification Point", default=1.0)

    @api.multi
    @api.onchange("type_id")
    def onchange_gamification_point(self):
        if not self.type_id:
            self.gamification_point = 1.0
            return
        self.gamification_point = self.type_id.gamification_point
