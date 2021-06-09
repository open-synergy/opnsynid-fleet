# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    passanger_sequence_id = fields.Many2one(
        string="Passanger Sequence",
        comodel_name="ir.sequence",
    )

    @api.multi
    def _get_passanger_sequence(self):
        self.ensure_one()

        if self.passanger_sequence_id:
            result = self.passanger_sequence_id
        else:
            result = self.env.ref("fleet_work_order_passanger.sequence_passanger")
        return result
