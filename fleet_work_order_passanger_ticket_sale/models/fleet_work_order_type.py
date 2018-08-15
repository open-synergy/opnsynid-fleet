# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FleetWorkOrderType(models.Model):
    _inherit = ["fleet.work.order.type"]

    default_passanger_pricelist_id = fields.Many2one(
        string="Default Passanger Ticket Pricelist",
        comodel_name="product.pricelist",
    )


class WorkOrderTypePassangerType(models.Model):
    _inherit = "fleet.work_order_type_passanger"
    _description = "Fleet Work Order Type Passanger"

    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=False,
    )
