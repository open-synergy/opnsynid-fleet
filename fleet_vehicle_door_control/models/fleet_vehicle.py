# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    door_ids = fields.One2many(
        string="Door(s)",
        comodel_name="fleet.vehicle.door",
        inverse_name="vehicle_id"
    )
