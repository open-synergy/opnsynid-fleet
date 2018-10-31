# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    @api.multi
    @api.depends(
        "type_id"
    )
    def _compute_allowed_picking_type_ids(self):
        for wo in self:
            wo.allowed_picking_type_ids = []
            if wo.type_id:
                wo.allowed_picking_type_ids = wo.type_id.picking_type_ids.ids

    @api.multi
    @api.depends(
        "type_id"
    )
    def _compute_allowed_partner_ids(self):
        for wo in self:
            wo.allowed_partner_ids = []
            if wo.type_id:
                wo.allowed_partner_ids = wo.type_id.partner_ids.ids

    @api.multi
    @api.depends(
        "type_id"
    )
    def _compute_restrict_partner_cargo(self):
        for wo in self:
            wo.restrict_partner_cargo = False
            if wo.type_id:
                wo.restrict_partner_cargo = wo.type_id.restrict_partner_cargo

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
