# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class FleetWorkOrderType(models.Model):
    _inherit = "fleet.work.order.type"

    passanger_sequence_id = fields.Many2one(
        string="Passanger Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    seat_required = fields.Boolean(
        string="Seat Selection Required?",
    )
    allow_stand = fields.Boolean(
        string="Allow Excess Passanger to Stand",
    )
    passanger_type_ids = fields.One2many(
        string="Passanger Types",
        comodel_name="fleet.work_order_type_passanger",
        inverse_name="wo_type_id",
    )


class WorkOrderTypePassangerType(models.Model):
    _name = "fleet.work_order_type_passanger"
    _description = "Fleet Work Order Type Passanger"

    wo_type_id = fields.Many2one(
        string="Work Order Type",
        comodel_name="fleet.work.order.type",
        required=False,
    )
    passanger_type_id = fields.Many2one(
        string="Passanger Type",
        comodel_name="fleet.work_order_passanger_type",
        required=True,
    )
