# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class FleetVehicleDoor(models.Model):
    _name = "fleet.vehicle.door"

    name = fields.Char(
        string="Name",
        required=True,
    )
    vehicle_id = fields.Many2one(
        string="Vehicle", comodel_name="fleet.vehicle", required=True
    )
    device_type_id = fields.Many2one(
        string="Device Type",
        comodel_name="proxy.backend_device_type",
        domain="[('door_control', '=', True)]",
    )
    door_control = fields.Boolean(string="Door Control")
    active = fields.Boolean(string="Active", default=True)
