# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    cargo_ids = fields.One2many(
        string="Cargo",
        comodel_name="shipment.plan",
        inverse_name="fleet_work_order_id",
        )

    
