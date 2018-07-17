# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class FleetVehicleDoor(models.Model):
    _inherit = "fleet.vehicle.door"

    name = fields.Char(
        string="Name",
        required=True,
        )
    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
        required=True
    )
    device_type_id = fields.Many2one(
        string="Device Type",
        comodel_name="proxy.backend_device_type",
        domain="[('door_control', '=', True)]"
    )
    device_id = fields.Many2one(
        string="Device",
        comodel_name="proxy.backend_device"
    )
    door_control = fields.Boolean(
        string="Door Control"
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )

    @api.onchange("device_type_id")
    def onchange_device_id(self):
        result = {
            "domain": {
                "device_id": [
                    ("id", "=", False)
                ]
            }
        }
        if self.device_type_id:
            result["domain"]["device_id"] = [
                ("type_id", "=", self.device_type_id.id)
            ]
        return result
