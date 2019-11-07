# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    debt_collection_id = fields.Many2one(
        string="A/R Collection",
        comodel_name="account.debt_collection",
    )

    @api.multi
    def button_cancel(self):
        _super = super(FleetWorkOrder, self)
        result = _super.button_cancel()
        for document in self:
            if document.debt_collection_id.state != "draft":
                msg = _("Debt Collection must be on <Draft> state")
                raise UserError(msg)
            document.debt_collection_id.unlink()
        return result

    @api.multi
    def _get_action_debt_collection(self):
        self.ensure_one()
        action =\
            self.env.ref(
                "account_debt_collection."
                "account_debt_collection_action").read()[0]
        return action

    @api.multi
    def action_view_debt_collection(self):
        self.ensure_one()
        action = self._get_action_debt_collection()

        action["domain"] =\
            [("id", "=", self.debt_collection_id.id)]

        return {
            "name": "A/R Collection",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "account.debt_collection",
            "res_id": self.debt_collection_id.id,
            "type": "ir.actions.act_window",
        }
