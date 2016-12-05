# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    in_wave_id = fields.Many2one(
        string="Wave In",
        comodel_name="stock.picking.wave",
        )

    @api.multi
    def action_add_in_wave(self):
        for order in self:
            self._create_in_wave()
            self._assign_in_picking_to_wave()

    @api.multi
    def action_reload_in_wave(self):
        for order in self:
            self._assign_in_picking_to_wave()

    @api.multi
    def _create_in_wave(self):
        self.ensure_one()
        if self.in_wave_id:
            strError = _("Wave in already exist")
            raise UserError(strError)

        obj_wave = self.env[
            "stock.picking.wave"]
        in_wave = obj_wave.create({})
        self.write({
            "in_wave_id": in_wave.id,
            })

    @api.multi
    def _assign_in_picking_to_wave(self):
        self.ensure_one()

        in_wave_pickings = self.in_wave_id.picking_ids
        departure_pickings = self.env[
            "stock.picking"].search([
                ("id","=",0),
                ])
        for shipment in self.cargo_ids:
            departure_pickings += shipment.departure_picking_ids
        # add to wave
        pickings = departure_pickings - in_wave_pickings
        pickings.write({
            "wave_id": self.in_wave_id.id,
            })
