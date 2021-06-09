# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    gamification_point = fields.Float(string="Gamification Point", default=1.0)

    @api.multi
    def _prepare_route_data(self, route):
        _super = super(FleetWorkOrder, self)
        res = _super._prepare_route_data(route)

        res["gamification_point"] = route.gamification_point

        return res
