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

    @api.multi
    def _check_cargo_ready(self):
        self.ensure_one()
        if not self.cargo_ids:
            return True

        for cargo in self.cargo_ids:
            strWarning = _("Cargo %s still not ready" % (cargo.name))
            if cargo.state != "in_transit":
                raise UserError(strWarning)

        return True

    @api.multi
    def _action_depart(self, 
                       date_depart=fields.Datetime.now(), 
                       starting_odometer=0.0):
        self.ensure_one()
        self._check_cargo_ready()

        super(FleetWorkOrder, self).button_depart(date_depart,
                                                  starting_odometer)
