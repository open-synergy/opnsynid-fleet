# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class FleetVehicleDoor(models.Model):
    _inherit = "fleet.vehicle.door"

    raspberry_relay_id = fields.Many2one(
        string="Raspberry Relay", comodel_name="proxy.backend_raspberry_relay"
    )
    device_raspberry_id = fields.Many2one(
        string="Raspberry Relay",
        related="raspberry_relay_id.device_id",
        comodel_name="proxy.backend_device",
        store=False,
    )
    channel = fields.Integer(
        string="Channel", related="raspberry_relay_id.pin", store=False
    )
