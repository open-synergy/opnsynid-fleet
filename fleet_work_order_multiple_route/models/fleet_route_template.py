# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class FleetRouteTemplate(models.Model):
    _name = "fleet.route.template"
    _description = "Fleet's Route Template"

    name = fields.Char(
        string="Name",
        required=True,
        readonly=False,
    )
    start_location_id = fields.Many2one(
        string="From",
        comodel_name="res.partner",
        required=True,
    )
    end_location_id = fields.Many2one(
        string="To",
        comodel_name="res.partner",
        required=True,
    )
    distance = fields.Float(
        string="Distance",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
