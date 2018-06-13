# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FleetWorkOrderPassangerSeat(models.Model):
    _name = "fleet.work_order_passanger_seat"
    _description = "Fleet Work Order Seat Passanger"

    work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order",
    )
    passanger_id = fields.Many2one(
        string="# Passanger",
        comodel_name="fleet.work_order_passanger",
        required=True,
    )
    seat_id = fields.Many2one(
        string="Seat",
        comodel_name="fleet.vehicle.seat",
        required=True,
    )
