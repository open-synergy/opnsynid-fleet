# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class PassangerBoardingDisembark(models.TransientModel):
    _inherit = "fleet.passanger_boarding_disembark"

    @api.multi
    @api.depends(
        "work_order_id")
    def _compute_onboard_ticket_sale(self):
        for wiz in self:
            ticket_ids = []
            passanger_type_ids =\
                self.work_order_id.type_id.passanger_type_ids
            if wiz.work_order_id.type_id.passanger_type_ids:
                for passanger_type in passanger_type_ids:
                    ticket_ids.append(passanger_type.id)
            wiz.onboard_ticket_sale_ids = [(6, 0, ticket_ids)]

    onboard_ticket_sale_ids = fields.Many2many(
        string="Available Onboard Tickets",
        comodel_name="fleet.work_order_type_passanger",
        compute="_compute_onboard_ticket_sale",
        )

    @api.multi
    def onboard_ticket_sale(self, passanger_type_id):
        self.ensure_one()
        obj_sale = self.env["fleet.work_order_passanger_ticket_sale"]

        obj_sale.create(self._prepare_onboard_ticket_sale_data())

    @api.multi
    def _prepare_onboard_ticket_sale_data(self):
        self.ensure_one()
        return {
            "work_order_id": self.work_order_id.id,
            "pricelist_id": self._get_onboard_ticket_pricelist_id(),
            }

    @api.multi
    def _get_onboard_ticket_pricelist_id(self):
        self.ensure_one()
        return self.work_order_id.default_passanger_pricelist_id or False
