# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order",
        copy=False,
    )
