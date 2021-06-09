# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class FleetVehicleDoor(models.Model):
    _inherit = "fleet.vehicle.door"

    serial_relay_id = fields.Many2one(
        string="Serial Relay", comodel_name="proxy.backend_serial_relay"
    )
    device_relay_id = fields.Many2one(
        string="Serial Relay",
        related="serial_relay_id.device_id",
        comodel_name="proxy.backend_device",
        store=False,
    )
    pin = fields.Integer(string="Pin", related="serial_relay_id.pin", store=False)
    device_path = fields.Char(
        string="Device Path", related="serial_relay_id.device_path", store=False
    )
