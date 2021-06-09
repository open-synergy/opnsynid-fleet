# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class FleetWorkOrderPassanger(models.Model):
    _inherit = ["fleet.work_order_passanger"]

    @api.multi
    @api.depends("price_unit", "tax_ids")
    def _compute_total(self):
        for passanger in self:
            passanger.price_subtotal = passanger.price_unit

    order_id = fields.Many2one(
        string="# Order",
        comodel_name="fleet.work_order_passanger_ticket_sale",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        domain=[
            ("key", "=", "passanger_ticket_sale"),
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    price_unit = fields.Float(
        string="Price Unit",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_passanger_2_tax",
        column1="passanger_id",
        column2="tax_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    price_subtotal = fields.Float(
        string="Subtotal",
        compute="_compute_total",
        store=True,
    )

    @api.onchange("pricelist_id")
    def onchange_currency_id(self):
        self.currency_id = False
        if self.pricelist_id:
            self.currency_id = self.pricelist_id.currency_id

    @api.onchange("type_id")
    def onchange_product_id(self):
        self.product_id = False
        if self.type_id:
            criteria = [
                ("passanger_type_id", "=", self.type_id.id),
                ("wo_type_id", "=", self.work_order_id.type_id.id),
            ]
            result = self.env["fleet.work_order_type_passanger"].search(criteria)
            if len(result) > 0:
                if result[0].product_id:
                    self.product_id = result[0].product_id.id

    @api.onchange(
        "product_id",
        "pricelist_id",
    )
    def onchange_price_unit(self):
        self.price_unit = 0.0
        if self.product_id and self.pricelist_id:
            self.price_unit = self.pricelist_id.price_get(
                prod_id=self.product_id.id, qty=1.0
            )[self.pricelist_id.id]

    @api.onchange("work_order_id")
    def onchange_type_id(self):
        self.type_id = False
        if (
            self.work_order_id
            and self.work_order_id.type_id
            and self.work_order_id.type_id.default_passanger_type_id
        ):
            self.type_id = self.work_order_id.type_id.default_passanger_type_id
