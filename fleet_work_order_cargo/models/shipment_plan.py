# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ShipmentPlan(models.Model):
    _inherit = "shipment.plan"

    fleet_work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order",
        readonly=True,
    )
