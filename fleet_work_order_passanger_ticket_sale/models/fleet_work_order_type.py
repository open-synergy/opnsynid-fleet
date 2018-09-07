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
    default_passanger_type_id = fields.Many2one(
        string="Default Passanger Type",
        comodel_name="fleet.work_order_passanger_type",
        )
    allowed_to_sell_group_ids = fields.Many2many(
        string="Allowed to Sell",
        comodel_name="res.groups",
        relation="rel_work_order_type_2_allowed_sale_group",
        column1="type_id",
        column2="group_id",
        )


class WorkOrderTypePassangerType(models.Model):
    _inherit = "fleet.work_order_type_passanger"
    _description = "Fleet Work Order Type Passanger"

    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=False,
    )
