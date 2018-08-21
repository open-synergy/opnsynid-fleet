# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FleetWorkOrderPassangerAnalysis(models.Model):
    _inherit = "fleet.work_order_passanger_analysis"

    price_after_tax = fields.Float(
        string="Price After Tax",
    )

    def _select(self):
        _super = super(FleetWorkOrderPassangerAnalysis, self)
        select_str = _super._select()
        select_str += """
            ,
            SUM(a.price_subtotal) AS price_after_tax
        """
        return select_str
