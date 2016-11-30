# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    in_wave_id = fields.Many2one(
        string="Wave In",
        comodel_name="stock.picking.wave",
        )

