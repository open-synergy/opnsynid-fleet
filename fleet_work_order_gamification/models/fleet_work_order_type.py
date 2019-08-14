# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FleetWorkOrderType(models.Model):
    _inherit = "fleet.work.order.type"

    gamification_point = fields.Float(
        string="Gamification Point",
        default=1.0
    )
