# -*- coding: utf-8 -*-
# Copyright 2016-2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class LoadWaveToCargo(models.TransientModel):
    _name = "fleet.load_wave_to_cargo"
    _description = "Load Wave to Cargo"

    wave_id = fields.Many2one(
        string="Wave",
        comodel_name="stock.picking.wave",
        domain=[
            ("state", "=", "done"),
        ],
    )

    @api.multi
    def action_load_cargo(self):
        for wiz in self:
            wiz._load_cargo()

    @api.multi
    def _load_cargo(self):
        self.ensure_one()
        wave = self.wave_id
        wo = self.env["fleet.work.order"].\
            browse([self.env.context.get("active_id", False)])[0]
        shipment_plans = wave.pickings_products.mapped(
            "departure_shipment_id")
        shipment_plans = shipment_plans.filtered(
            lambda r: not r.fleet_work_order_id and r.state == "confirmed")
        shipment_plans.write({
            "fleet_work_order_id": wo.id,
        })
