# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class FleetWorkOrderPassangerTicketSale(models.Model):
    _name = "fleet.work_order_passanger_ticket_sale"
    _inherit = ["mail.thread"]
    _description = "Fleet Work Order Passanger Ticket Sale"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id

    @api.model
    def _default_date_order(self):
        return fields.Datetime.now()

    @api.model
    def _default_pricelist_id(self):
        wo_id = self._context.get("default_work_order_id", False)

        result = False
        if wo_id:
            wo = self.env["fleet.work.order"].browse([wo_id])[0]
            if wo.type_id and wo.type_id.default_passanger_pricelist_id:
                result = wo.type_id.default_passanger_pricelist_id.id
        return result

    @api.multi
    @api.depends(
        "passanger_ids",
        "passanger_ids.price_unit",
    )
    def _compute_total(self):
        for sale in self:
            amount_before_tax = amount_tax = amount_after_tax = 0.0

            for passanger in sale.passanger_ids:
                amount_before_tax = passanger.price_subtotal

            amount_after_tax = amount_before_tax + amount_tax
            sale.amount_before_tax = amount_before_tax
            sale.amount_tax = amount_tax
            sale.amount_after_tax = amount_after_tax

    name = fields.Char(
        string="# Order",
        default="/",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        required=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        track_visibility="onchange",
    )
    work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        track_visibility="onchange",
    )
    date_order = fields.Datetime(
        string="Date Order",
        default=lambda self: self._default_date_order(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        track_visibility="onchange",
    )
    partner_id = fields.Many2one(
        string="Invoice To",
        comodel_name="res.partner",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        domain=[
            ("customer", "=", True),
        ],
        track_visibility="onchange",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        domain=[
            ("type", "=", "passanger_ticket_sale"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        track_visibility="onchange",
        default=lambda self: self._default_pricelist_id(),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="pricelist_id.currency_id",
        store=True,
    )
    passanger_ids = fields.One2many(
        string="Passangers",
        comodel_name="fleet.work_order_passanger",
        inverse_name="order_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_before_tax = fields.Float(
        string="Amount Before Tax",
        compute="_compute_total",
        store=True,
    )
    amount_tax = fields.Float(
        string="Amount Tax",
        compute="_compute_total",
        store=True,
    )
    amount_after_tax = fields.Float(
        string="Amount After Tax",
        compute="_compute_total",
        store=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Validation"),
            ("valid", "Valid"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        readonly=True,
        required=True,
        track_visibility="onchange",
    )

    @api.multi
    def action_confirm(self):
        for sale in self:
            sale.write(self._prepare_confirm_data())
            # sale.passanger_ids.action_confirm()

    @api.multi
    def action_valid(self):
        for sale in self:
            sale.write(self._prepare_valid_data())
            # sale.passanger_ids.action_valid()

    @api.multi
    def action_cancel(self):
        for sale in self:
            sale.write(self._prepare_cancel_data())
            # sale.passanger_ids.action_cancel()

    @api.multi
    def action_restart(self):
        for sale in self:
            sale.write(self._prepare_restart_data())
            # sale.passanger_ids.action_restart()

    @api.multi
    def action_buy_simple(self):
        self.ensure_one()
        self.write(self._prepare_confirm_data())
        # self.passanger_ids.action_confirm()
        self.write(self._prepare_valid_data())
        # self.passanger_ids.action_valid()
        return self._reload_simple_screen()

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
        }

    @api.multi
    def _prepare_valid_data(self):
        self.ensure_one()
        return {
            "state": "valid",
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.multi
    def _reload_simple_screen(self):
        self.ensure_one()
        waction = self.env.ref(
            "fleet_work_order_passanger_ticket_sale."
            "fleet_work_order_passanger_ticket_sale_simple_action"
        ).read()[0]
        waction.update(
            {
                "res_id": self.id,
            }
        )
        return waction

    @api.onchange("work_order_id")
    def oncange_pricelist_id(self):
        self.pricelist_id = False
        if (
            self.work_order_id
            and self.work_order_id.type_id
            and self.work_order_id.type_id.default_passanger_pricelist_id
        ):
            self.pricelist_id = (
                self.work_order_id.type_id.default_passanger_pricelist_id.id
            )

    @api.multi
    def print_ticket(self):
        company = self.env.user.company_id
        aeroo_ticket = company.default_aeroo_ticket
        if aeroo_ticket:
            if self.passanger_ids:
                action = self.env.ref(
                    "proxy_backend_ecspos_aeroo." "proxy_backend_ecspos_aeroo_action"
                )
                context = {
                    "report_name": aeroo_ticket.report_name,
                    "object_id": self.passanger_ids.ids,
                }
                result = action.read()[0]
                result.update({"context": context})
                return result
            else:
                raise UserError(_("No Passangers"))
        else:
            raise UserError(_("No Aeroo Ticket Defined in Company"))
