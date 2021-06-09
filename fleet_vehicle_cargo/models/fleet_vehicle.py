# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    cargo = fields.Boolean(
        string="Cargo?",
    )
    floor_space = fields.Float(
        string="Floor Space",
    )
    floor_space_uom_id = fields.Many2one(
        string="Floor Space UoM",
        comodel_name="product.uom",
    )
    loading_space = fields.Float(
        string="Loading Space",
    )
    loading_space_uom_id = fields.Many2one(
        string="Loading Space UoM",
        comodel_name="product.uom",
    )
    load_capacity = fields.Float(
        string="Load Capacity",
    )
    load_capacity_uom_id = fields.Many2one(
        string="Load Capacity UoM",
        comodel_name="product.uom",
    )
