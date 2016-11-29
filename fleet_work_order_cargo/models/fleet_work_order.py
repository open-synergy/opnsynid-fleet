# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    @api.depends(
        "vehicle_id",
        "vehicle_id.loading_space",
        "vehicle_id.load_capacity",
        "cargo_ids",
        "cargo_ids.volume",
        "cargo_ids.weight",
        "cargo_ids.weight_net")
    def _compute_cargo(self):
        for order in self:
            order.weight_diff = 0.0
            order.volume_diff = 0.0
            for cargo in order.cargo_ids:
                order.cargo_volume += cargo.volume
                order.cargo_weight += cargo.weight
            order.weight_diff = order.loading_space - \
                order.cargo_volume
            order.volume_diff = order.load_capacity - \
                order.cargo_weight

    cargo_ids = fields.One2many(
        string="Cargo",
        comodel_name="shipment.plan",
        inverse_name="fleet_work_order_id",
    )

    loading_space = fields.Float(
        string="Loading Space",
        related="vehicle_id.loading_space",
        store=True,
        readonly=False,
    )
    load_capacity = fields.Float(
        string="Load Capacity",
        related="vehicle_id.load_capacity",
        store=True,
        readonly=False,
    )
    cargo_volume = fields.Float(
        string="Cargo Volume",
        compute="_compute_cargo",
        store=True,
    )
    cargo_weight = fields.Float(
        string="Cargo Weight",
        compute="_compute_cargo",
        store=True,
    )
    weight_diff = fields.Float(
        string="Cargo Weight Diff",
        compute="_compute_cargo",
        store=True,
    )
    volume_diff = fields.Float(
        string="Cargo Volume Diff",
        compute="_compute_cargo",
        store=True,
    )
    cargo_limit_override = fields.Boolean(
        string="Cargo Limit Override",
    )

    @api.constrains(
        "state", "cargo_ids")
    def _constraint_cargo(self):
        if not self.cargo_ids:
            pass

        if self.state == "depart":
            for cargo in self.cargo_ids:
                strWarning = _("Cargo %s still not ready" % (cargo.name))
                if cargo.state != "in_transit":
                    raise UserError(strWarning)
        elif self.state == "arrive":
            for cargo in self.cargo_ids:
                strWarning = _("Cargo %s still not done" % (cargo.name))
                if cargo.state != "done":
                    raise UserError(strWarning)
