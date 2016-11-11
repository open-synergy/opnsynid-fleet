# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class FleetWorkOrder(models.Model):
    _inherit = "fleet.work.order"

    cargo_ids = fields.One2many(
        string="Cargo",
        comodel_name="shipment.plan",
        inverse_name="fleet_work_order_id",
    )

    @api.constrains(
        "state", "cargo_ids")
    def _constraint_cargo(self):
        if not self.cargo_ids:
            pass

        if self.state == "depart":
            for cargo in self.cargo_ids:
                strWarning = _("Cargo %s still not ready" % (cargo.name))
                if cargo.state != "in_transit":
                    raise UserError(strWarning)
        elif self.state == "arrive":
            for cargo in self.cargo_ids:
                strWarning = _("Cargo %s still not done" % (cargo.name))
                if cargo.state != "done":
                    raise UserError(strWarning)
