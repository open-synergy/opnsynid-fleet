# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models

DOMAIN_AEROO = [("report_type", "=", "aeroo"), ("in_format", "=", "genshi-raw")]


class ResCompany(models.Model):
    _inherit = "res.company"

    default_aeroo_ticket = fields.Many2one(
        string="Aeroo Ticket",
        comodel_name="ir.actions.report.xml",
        domain=DOMAIN_AEROO,
        company_dependent=True,
    )
