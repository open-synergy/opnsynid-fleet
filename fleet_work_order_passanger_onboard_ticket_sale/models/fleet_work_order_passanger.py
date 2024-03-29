# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class FleetWorkOrderPassanger(models.Model):
    _inherit = ["fleet.work_order_passanger"]

    onboard_sale = fields.Boolean(
        string="Onboard Sale",
        readonly=True,
    )
