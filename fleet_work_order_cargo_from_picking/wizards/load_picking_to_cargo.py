# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class LoadPickingToCargo(models.TransientModel):
    _name = "fleet.load_picking_to_cargo"
    _description = "Load Picking to Cargo"

    @api.multi
    @api.depends(
        "work_order_id",
    )
    def _compute_allowed_picking_type_ids(self):
        for wiz in self:

            wiz.allowed_picking_type_ids = []
            if wiz.work_order_id.type_id:
                wiz.allowed_picking_type_ids = (
                    wiz.work_order_id.type_id.picking_type_ids.ids
                )

    @api.multi
    @api.depends(
        "work_order_id",
    )
    def _compute_allowed_partner_ids(self):
        for wiz in self:

            wiz.allowed_partner_ids = []
            if wiz.work_order_id.type_id:
                wiz.allowed_partner_ids = wiz.work_order_id.type_id.partner_ids.ids

    @api.multi
    @api.depends("work_order_id")
    def _compute_restrict_partner_cargo(self):
        for wiz in self:
            wiz.restrict_partner_cargo = False
            if wiz.work_order_id.type_id:
                wiz.restrict_partner_cargo = (
                    wiz.work_order_id.type_id.restrict_partner_cargo
                )

    @api.model
    def _default_work_order_id(self):
        return self.env.context.get("active_id", False)

    work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order",
        default=lambda self: self._default_work_order_id(),
    )
    picking_ids = fields.Many2many(
        string="Pickings",
        comodel_name="stock.picking",
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

    @api.multi
    def action_load_cargo(self):
        for wiz in self:
            wiz._load_cargo()

    @api.multi
    def _load_cargo(self):
        self.ensure_one()
        for picking in self.picking_ids:
            picking.move_lines._compute_measurement()
        self.picking_ids._compute_measurement()
        self.picking_ids.write({"work_order_id": self.work_order_id.id})
