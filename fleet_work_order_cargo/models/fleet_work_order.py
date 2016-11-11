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
            for cargo in order.cargo_ids:
                order.cargo_volume += cargo.volume
                order.cargo_weight += cargo.weight

    cargo_ids = fields.One2many(
        string="Cargo",
        comodel_name="shipment.plan",
        inverse_name="fleet_work_order_id",
    )
    
    loading_space = fields.Float(
        string="Loading Space",
        related="vehicle_id.loading_space",
        )
    load_capacity = fields.Float(
        string="Load Capacity",
        related="vehicle_id.load_capacity",
        )
    cargo_volume = fields.Float(
        string="Cargo Volume",
        compute="_compute_cargo",
        )
    cargo_weight = fields.Float(
        string="Cargo Weight",
        compute="_compute_cargo",
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
