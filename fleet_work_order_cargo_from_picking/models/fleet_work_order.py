# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    @api.multi
    @api.depends("type_id")
    def _compute_allowed_picking_type_ids(self):
        for wo in self:
            wo.allowed_picking_type_ids = []
            if wo.type_id:
                wo.allowed_picking_type_ids = wo.type_id.picking_type_ids.ids

    @api.multi
    @api.depends("type_id")
    def _compute_allowed_partner_ids(self):
        for wo in self:
            wo.allowed_partner_ids = []
            if wo.type_id:
                wo.allowed_partner_ids = wo.type_id.partner_ids.ids

    @api.multi
    @api.depends("type_id")
    def _compute_restrict_partner_cargo(self):
        for wo in self:
            wo.restrict_partner_cargo = False
            if wo.type_id:
                wo.restrict_partner_cargo = wo.type_id.restrict_partner_cargo

    @api.depends(
        "vehicle_id",
        "vehicle_id.loading_space",
        "vehicle_id.load_capacity",
        "picking_ids",
        "picking_ids.move_lines",
        "picking_ids.move_lines.product_id",
        "picking_ids.move_lines.product_qty",
    )
    def _compute_picking(self):
        for order in self:
            picking_volume = (
                picking_weight
            ) = picking_weight_diff = picking_volume_diff = 0.0
            for picking in order.picking_ids:
                for move in picking.move_lines:
                    picking_volume += move.product_id.volume * move.product_qty
                    picking_weight += move.product_id.weight * move.product_qty
            picking_volume_diff = order.loading_space - picking_volume
            picking_weight_diff = order.load_capacity - picking_weight
            order.picking_volume = picking_volume
            order.picking_weight = picking_weight
            order.picking_volume_diff = picking_volume_diff
            order.picking_weight_diff = picking_weight_diff

    picking_volume = fields.Float(
        string="Picking Volume",
        compute="_compute_picking",
        store=True,
    )
    picking_weight = fields.Float(
        string="Picking Weight",
        compute="_compute_picking",
        store=True,
    )
    picking_weight_diff = fields.Float(
        string="Picking Weight Diff",
        compute="_compute_picking",
        store=True,
    )
    picking_volume_diff = fields.Float(
        string="Picking Volume Diff",
        compute="_compute_picking",
        store=True,
    )

    @api.depends(
        "loading_space",
        "load_capacity",
        "picking_volume",
        "picking_weight",
    )
    def _compute_picking_progress(self):
        for order in self:
            progress_volume = progress_weight = 0.0
            try:
                progress_volume = (order.picking_volume / order.loading_space) * 100
            except ZeroDivisionError:
                progress_volume = 0.0
            try:
                progress_weight = (order.picking_weight / order.load_capacity) * 100
            except ZeroDivisionError:
                progress_weight = 0.0
            order.picking_volume_progress = progress_volume
            order.picking_weight_progress = progress_weight

    picking_volume_progress = fields.Float(
        string="Progress Volume",
        compute="_compute_picking_progress",
        store=True,
    )
    picking_weight_progress = fields.Float(
        string="Progress Weight",
        compute="_compute_picking_progress",
        store=True,
    )
    picking_ids = fields.One2many(
        string="Pickings",
        comodel_name="stock.picking",
        inverse_name="work_order_id",
        copy=False,
    )
    allowed_picking_type_ids = fields.Many2many(
        string="Allowed Picking Types",
        comodel_name="stock.picking.type",
        compute="_compute_allowed_picking_type_ids",
        store=False,
    )
    restrict_partner_cargo = fields.Boolean(
        string="Restrict Partner Cargo",
        compute="_compute_restrict_partner_cargo",
        store=False,
    )
    allowed_partner_ids = fields.Many2many(
        string="Allowed Cargo Partner",
        comodel_name="res.partner",
        compute="_compute_allowed_partner_ids",
        store=False,
    )
    picking_summary_ids = fields.One2many(
        string="Picking Summary",
        comodel_name="fleet.work.order.picking_summary",
        inverse_name="work_order_id",
    )
