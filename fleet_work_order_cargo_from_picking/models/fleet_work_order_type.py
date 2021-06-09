# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class FleetWorkOrderType(models.Model):
    _inherit = "fleet.work.order.type"

    picking_type_ids = fields.Many2many(
        string="Allowed Picking Types",
        comodel_name="stock.picking.type",
        relation="rel_flet_work_order_type_2_picking_type",
        column1="fleet_wo_type_id",
        column2="picking_type_id",
    )
    restrict_partner_cargo = fields.Boolean(
        string="Restrict Partner Cargo",
    )
    partner_ids = fields.Many2many(
        string="Allowed Partners",
        comodel_name="res.partner",
        relation="rel_fleet_work_order_type_2_partner",
        column1="type_id",
        column2="partner_id",
    )
