# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class FleetRouteTemplate(models.Model):
    _inherit = "fleet.route.template"

    gamification_point = fields.Float(string="Gamification Point", default=1.0)
