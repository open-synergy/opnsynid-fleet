# -*- coding: utf-8 -*-
# © © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    agent_id = fields.Many2one(
        string="Agent",
        comodel_name="res.partner",
        domain=[
            ("is_fleet_agent", "=", True),
        ],
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
    )
