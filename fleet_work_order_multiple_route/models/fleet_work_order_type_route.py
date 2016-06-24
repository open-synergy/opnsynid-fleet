# -*- coding: utf-8 -*-
# © © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class WorkOrderTypeRoute(models.Model):
    _description = 'Work Order Type Route'
    _name = 'fleet.work.order.type.route'

    name = fields.Char(
        string='Name',
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
    )
    type_id = fields.Many2one(
        string='Work Order Type',
        comodel_name='fleet.work.order.type',
    )
    route_template_id = fields.Many2one(
        comodel_name="fleet.route.template",
        string="Route Template",
    )
    start_location_id = fields.Many2one(
        string='From',
        comodel_name='res.partner',
        required=True,
    )
    end_location_id = fields.Many2one(
        string='To',
        comodel_name='res.partner',
        required=True,
    )
    distance = fields.Float(
        string="Distance",
        required=True,
    )

    @api.onchange('route_template_id')
    def onchange_route_template(self):
        if self.route_template_id:
            template = self.route_template_id
            self.start_location_id = template.start_location_id.id
            self.end_location_id = template.end_location_id.id
            self.distance = template.distance
            self.name = template.name


class WorkOrderType(models.Model):
    _inherit = 'fleet.work.order.type'

    @api.one
    @api.depends('multiple_route', 'route_ids')
    def _compute_route(self):
        if self.multiple_route and len(self.route_ids) > 0:
            self.function_start_location_id = self.route_ids[
                0].start_location_id.id
            self.function_end_location_id = self.route_ids[
                -1].end_location_id.id
            for route in self.route_ids:
                self.function_distance += route.distance
        else:
            self.function_start_location_id = self.start_location_id.id
            self.function_end_location_id = self.end_location_id.id
            self.function_distance = self.distance

    route_ids = fields.One2many(
        string='Routes',
        comodel_name='fleet.work.order.type.route',
        inverse_name='type_id',
    )

    multiple_route = fields.Boolean(
        string='Multiple Routes',
    )

    function_start_location_id = fields.Many2one(
        string='Start Location',
        comodel_name='res.partner',
        compute='_compute_route',
        store=True,
        readonly=True,
    )

    function_end_location_id = fields.Many2one(
        string='End Location',
        comodel_name='res.partner',
        compute='_compute_route',
        store=True,
        readonly=True,
    )

    function_distance = fields.Float(
        string='Distance',
        compute='_compute_route',
        store=True,
        readonly=True,
    )
