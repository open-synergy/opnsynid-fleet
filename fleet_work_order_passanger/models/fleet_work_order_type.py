# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FleetWorkOrderType(models.Model):
    _inherit = "fleet.work.order.type"

    passanger_sequence_id = fields.Many2one(
        string="Passanger Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    seat_required = fields.Boolean(
        string="Seat Selection Required?",
    )
    allow_stand = fields.Boolean(
        string="Allow Excess Passanger to Stand",
    )
