# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    @api.multi
    @api.depends("multiple_route", "route_ids")
    def _compute_route(self):
        for document in self:
            if document.multiple_route and len(document.route_ids) > 0:
                document.function_start_location_id = document.route_ids[
                    0
                ].start_location_id.id
                document.function_end_location_id = document.route_ids[
                    -1
                ].end_location_id.id
                for route in document.route_ids:
                    document.function_distance += route.distance
            else:
                document.function_start_location_id = document.start_location_id.id
                document.function_end_location_id = document.end_location_id.id
                document.function_distance = document.distance

    route_ids = fields.One2many(
        string="Routes",
        comodel_name="fleet.route",
        inverse_name="order_id",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    multiple_route = fields.Boolean(
        string="Multiple Routes",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    function_start_location_id = fields.Many2one(
        string="Start Location",
        comodel_name="res.partner",
        compute="_compute_route",
        store=True,
        readonly=True,
    )

    function_end_location_id = fields.Many2one(
        string="End Location",
        comodel_name="res.partner",
        compute="_compute_route",
        store=True,
        readonly=True,
    )

    function_distance = fields.Float(
        string="Distance",
        compute="_compute_route",
        store=True,
        readonly=True,
    )

    @api.onchange("type_id")
    def onchange_multiple_route(self):
        if self.type_id:
            wo_type = self.type_id
            self.multiple_route = wo_type.multiple_route

    @api.onchange("type_id")
    def onchange_route_ids(self):
        self.route_ids.unlink()
        if self.type_id:
            wo_type = self.type_id
            if wo_type.route_ids:
                routes = []
                for route in wo_type.route_ids:
                    res = self._prepare_route_data(route)
                    routes.append((0, 0, res))
                self.route_ids = routes

    @api.multi
    def _prepare_route_data(self, route):
        self.ensure_one()
        result = {
            "name": route.name,
            "sequence": route.sequence,
            "route_template_id": route.route_template_id.id,
            "start_location_id": route.start_location_id.id,
            "end_location_id": route.end_location_id.id,
            "distance": route.distance,
        }
        return result
