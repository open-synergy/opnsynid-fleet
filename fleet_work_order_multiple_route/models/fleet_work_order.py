# -*- coding: utf-8 -*-
# © © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

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
        string="Routes",
        comodel_name="fleet.route",
        inverse_name="order_id",
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
    )

    multiple_route = fields.Boolean(
        string='Multiple Routes',
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
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
        string='End Location',
        compute='_compute_route',
        store=True,
        readonly=True,
    )

    @api.onchange('type_id')
    def onchange_type_id(self):
        self.vehicle_id = False
        self.driver_id = False
        self.co_driver_id = False
        self.route_ids.unlink()
        if self.type_id:
            wo_type = self.type_id
            self.vehicle_id = wo_type.vehicle_id and \
                wo_type.vehicle_id.id or False
            self.driver_id = wo_type.driver_id and \
                wo_type.driver_id.id or False
            self.co_driver_id = wo_type.co_driver_id and \
                wo_type.co_driver_id.id or False
            self.start_location_id = wo_type.start_location_id and \
                wo_type.start_location_id.id or False
            self.end_location_id = wo_type.end_location_id and \
                wo_type.end_location_id.id or False
            self.distance = wo_type.distance
            self.multiple_route = wo_type.multiple_route
            if wo_type.route_ids:
                routes = []
                for route in wo_type.route_ids:
                    res = {
                        'name': route.name,
                        'sequence': route.sequence,
                        'route_template_id': route.route_template_id.id,
                        'start_location_id': route.start_location_id.id,
                        'end_location_id': route.end_location_id.id,
                        'distance': route.distance,
                    }
                    routes.append((0, 0, res))
                self.route_ids = routes
