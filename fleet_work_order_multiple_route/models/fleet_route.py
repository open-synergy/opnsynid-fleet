# -*- coding: utf-8 -*-
# © © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class FleetRoute(models.Model):
    _name = "fleet.route"
    _description = "Fleet Route"
    _order = "sequence"

    name = fields.Char(
        string="Route",
        required=True,
    )
    order_id = fields.Many2one(
        string="# Order",
        comodel_name="fleet.work.order",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
    )
    route_template_id = fields.Many2one(
        string="Route Template",
        comodel_name="fleet.route.template",
        required=False,
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

    @api.onchange("route_template_id")
    def onchange_route_template_id(self):
        if self.route_template_id:
            route_template = self.route_template_id
            self.start_location_id = route_template.start_location_id.id
            self.end_location_id = route_template.end_location_id.id
            self.distance = route_template.distance
            self.name = route_template.name
        else:
            self.start_location_id = False
            self.end_location_id = False
            self.distance = 0.0
