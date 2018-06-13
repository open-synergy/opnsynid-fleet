# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    passanger_ids = fields.One2many(
        string="Passangers",
        comodel_name="fleet.work_order_passanger",
        inverse_name="work_order_id",
    )

    @api.multi
    def _get_passanger_sequence(self):
        self.ensure_one()

        if self.type_id and \
                self.type_id.passanger_sequence_id:
            result = self.type_id.passanger_sequence_id
        else:
            result = self.env.user.company_id._get_passanger_sequence()
        return result
