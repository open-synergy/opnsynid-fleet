# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from datetime import datetime
from openerp.exceptions import Warning as UserError


class FleetDebtCollectionCreate(models.TransientModel):
    _name = "fleet.debt_collection_create"
    _description = "Wizard Create Debt Collection From Work Order"

    @api.model
    def _default_work_order_id(self):
        active_id =\
            self.env.context.get("active_id", False)
        return active_id

    work_order_id = fields.Many2one(
        string="#Work Order",
        comodel_name="fleet.work.order",
        default=lambda self: self._default_work_order_id(),
    )

    @api.model
    def _default_date(self):
        return fields.Date.today()

    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: self._default_date(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    collection_type_id = fields.Many2one(
        string="Type",
        comodel_name="account.debt_collection_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    collector_id = fields.Many2one(
        string="Collector",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def _compute_allowed_invoice_ids(self):
        allowed_invoice_ids =\
            self.env.context.get("allowed_invoice_ids", False)

        for document in self:
            document.allowed_invoice_ids = allowed_invoice_ids

    allowed_invoice_ids = fields.Many2many(
        string="Allowed Invoices",
        comodel_name="account.invoice",
        compute="_compute_allowed_invoice_ids",
        store=False,
    )
    invoice_ids = fields.Many2many(
        string="Invoices",
        comodel_name="account.invoice",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('draft', 'Draft'),
            ('invoice', 'Invoice'),
            ('success', 'Success'),
            ('failed_invoice', 'Invoice Failed'),
            ('failed', 'Failed'),
        ],
        default="draft"
    )

    @api.multi
    @api.onchange(
        "collection_type_id"
    )
    def onchange_collector_id(self):
        allowed_collector_ids = []
        if self.collection_type_id:
            allowed_collector_ids =\
                self.collection_type_id.allowed_collector_ids.ids
        return {
            "domain": {
                "collector_id": [("id", "in", allowed_collector_ids)]
            }
        }

    @api.multi
    def action_create_collection(self):
        self.ensure_one()
        obj_debt_collection = self.env["account.debt_collection"]
        obj_debt_collection_detail =\
            self.env["account.debt_collection_detail"]
        document = self.work_order_id

        if not self._check_debt_collection():
            msg = _("Debt Collection has been created with number: %s")
            raise UserError(msg % (document.debt_collection_id.name))

        if self.invoice_ids:
            debt_collection_id =\
                obj_debt_collection.create(
                    self._prepare_debt_collection_header()
                )
            for invoice in self.invoice_ids:
                detail_id = obj_debt_collection_detail.create(
                    self._prepare_debt_collection_detail(
                        debt_collection_id,
                        invoice
                    )
                )
                detail_id.onchange_amount_due()
            document.write({
                "debt_collection_id": debt_collection_id.id
            })
            vals = {
                "state": "success",
            }
            self.write(vals)

        return {
            "type": "ir.actions.act_window",
            "res_model": str(self._model),
            "view_mode": "form",
            "view_type": "form",
            "res_id": self.id,
            "views": [(False, "form")],
            "target": "new",
        }

    @api.multi
    def action_generate_invoice(self):
        self.ensure_one()
        obj_account_invoice = self.env["account.invoice"]

        invoice_ids =\
            obj_account_invoice.search(
                self._prepare_criteria_invoice())
        if invoice_ids:
            vals = {
                "invoice_ids": [(6, 0, invoice_ids.ids)],
                "state": "invoice",
            }
        else:
            vals = {
                "state": "failed_invoice",
            }
        self.write(vals)

        return {
            "type": "ir.actions.act_window",
            "res_model": str(self._model),
            "view_mode": "form",
            "view_type": "form",
            "res_id": self.id,
            "views": [(False, "form")],
            "context": {
                "allowed_invoice_ids": invoice_ids.ids
            },
            "target": "new",
        }

    @api.multi
    def _prepare_debt_collection_header(self):
        self.ensure_one()
        note = "Create from %s" % (self.work_order_id.name)
        return {
            "collection_type_id": self.collection_type_id.id,
            "collector_id": self.collector_id.id,
            "note": note,
        }

    @api.multi
    def _prepare_debt_collection_detail(
        self,
        debt_collection_id,
        invoice
    ):
        self.ensure_one()
        return {
            "debt_collection_id": debt_collection_id.id,
            "invoice_id": invoice.id,
        }

    @api.multi
    def _prepare_criteria_invoice(self):
        self.ensure_one()
        obj_debt_collection = self.env["account.debt_collection"]
        result = [
            ("id", "=", 0)
        ]
        collection_type =\
            self.collection_type_id
        allowed_journal_ids =\
            collection_type.allowed_journal_ids.ids
        date = datetime.strptime(self.date, "%Y-%m-%d")
        days_after_due =\
            collection_type.days_after_due
        days_before_due =\
            collection_type.days_before_due

        date_after_invoice_due =\
            obj_debt_collection._get_date_after_invoice_due(
                date, days_after_due).strftime("%Y-%m-%d")
        date_before_invoice_due =\
            obj_debt_collection._get_date_before_invoice_due(
                date, days_before_due).strftime("%Y-%m-%d")

        if allowed_journal_ids:
            criteria = [
                ("state", "=", "open"),
                ("type", "=", "out_invoice"),
                ("journal_id", "in", allowed_journal_ids),
                ("date_due", ">=", date_before_invoice_due),
                ("date_due", "<=", date_after_invoice_due),
            ]
        if self.work_order_id.multiple_route:
            partner_ids =\
                self.work_order_id.mapped("route_ids.end_location_id")
            criteria_partner = [
                ("partner_id", "in", partner_ids.ids),
            ]
            result = criteria + criteria_partner
        else:
            criteria_partner = [
                ("partner_id", "=", self.work_order_id.end_location_id.id),
            ]
            result = criteria + criteria_partner
        return result

    @api.multi
    def _check_debt_collection(self):
        self.ensure_one()
        result = True
        if self.work_order_id.debt_collection_id:
            result = False
        return result
