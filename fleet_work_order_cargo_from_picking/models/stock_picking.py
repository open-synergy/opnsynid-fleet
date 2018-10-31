# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order",
        copy=False,
    )
