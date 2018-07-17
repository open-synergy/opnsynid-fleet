# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class FleetVehicleDoor(models.Model):
    _name = "fleet.vehicle.door"

    name = fields.Char(
        string="Name",
        required=True,
    )
    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
        required=True
    )
    serial_relay_id = fields.Many2one(
        string="Serial Relay",
        comodel_name="proxy.backend_serial_relay",
        domain="[('type_id.door_control', '=', True)]"
    )
    str_serial_relay_id = fields.Char(
        string="Serial Relay ID"
    )
    serial_relay_channel_id = fields.Many2one(
        string="Channel",
        comodel_name="proxy.backend_serial_relay_channel"
    )
    str_serial_relay_channel_name = fields.Char(
        string="Channel Name"
    )
    door_control = fields.Boolean(
        string="Door Control"
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )

    @api.onchange("serial_relay_id")
    def onchange_serial_relay_channel_id(self):
        result = {
            "domain": {
                "serial_relay_channel_id": [
                    ("id", "=", False)
                ]
            }
        }
        str_serial_relay_id = ""
        if self.serial_relay_id:
            result["domain"]["serial_relay_channel_id"] = [
                ("device_id", "=", self.serial_relay_id.id)
            ]
            str_serial_relay_id = self.serial_relay_id.id
        self.str_serial_relay_id = str_serial_relay_id
        return result

    @api.onchange("serial_relay_channel_id")
    def onchange_str_serial_relay_channel_name(self):
        str_serial_relay_channel_name = ""
        if self.serial_relay_channel_id:
            str_serial_relay_channel_name =\
                self.serial_relay_channel_id.name
        self.str_serial_relay_channel_name =\
            str_serial_relay_channel_name
