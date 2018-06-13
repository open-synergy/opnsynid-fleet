# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.exceptions import Warning as UserError, ValidationError
from openerp.tools.translate import _


class FleetWorkOrderPassanger(models.Model):
    _name = "fleet.work_order_passanger"
    _inherit = ["mail.thread"]
    _description = "Fleet Work Order Passanger"

    work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
        related="work_order_id.vehicle_id",
    )
    name = fields.Char(
        string="# Passanger",
        default="/",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        required=False,
        track_visibility="onchange",
    )
    start_location_id = fields.Many2one(
        string="Start Location",
        comodel_name="res.partner",
        readonly=True,
        states={
            'draft': [
                ('readonly', False),
            ],
        },
        track_visibility="onchange",
    )
    end_location_id = fields.Many2one(
        string="End Location",
        comodel_name="res.partner",
        readonly=True,
        states={
            'draft': [
                ('readonly', False),
            ],
        },
        track_visibility="onchange",
    )
    type_id = fields.Many2one(
        string="Passanger Type",
        comodel_name="fleet.work_order_passanger_type",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        required=True,
        track_visibility="onchange",
    )
    seat_id = fields.Many2one(
        string="Seat",
        comodel_name="fleet.vehicle.seat",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        track_visibility="onchange",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Validation"),
            ("valid", "Valid"),
            ("boarding", "Boarding"),
            ("disembarking", "Disembarking"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        readonly=True,
        required=True,
        track_visibility="onchange",
    )

    @api.multi
    def action_confirm(self):
        for passanger in self:
            passanger.write(passanger._prepare_confirm_data())

    @api.multi
    def action_valid(self):
        for passanger in self:
            passanger.write(passanger._prepare_valid_data())

    @api.multi
    def action_boarding(self):
        for passanger in self:
            passanger.write(passanger._prepare_boarding_data())

    @api.multi
    def action_disembarking(self):
        for passanger in self:
            passanger.write(passanger._prepare_disembarking_data())

    @api.multi
    def action_cancel(self):
        for passanger in self:
            passanger.write(passanger._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for passanger in self:
            passanger.write(passanger._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
        }

    @api.multi
    def _prepare_valid_data(self):
        self.ensure_one()
        return {
            "state": "valid",
        }

    @api.multi
    def _prepare_boarding_data(self):
        self.ensure_one()
        return {
            "state": "boarding",
        }

    @api.multi
    def _prepare_disembarking_data(self):
        self.ensure_one()
        return {
            "state": "disembarking",
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.multi
    def _prepare_create_data(self, value):
        return value

    @api.multi
    def _get_sequence(self):
        self.ensure_one()

        result = self.work_order_id._get_passanger_sequence()

        return result

    @api.multi
    def _create_sequence(self):
        self.ensure_one()
        if self._check_sequence:
            name = self.env["ir.sequence"].\
                next_by_id(self._get_sequence().id) or "/"
            self.write({"name": name})

    @api.multi
    def _check_sequence(self):
        self.ensure_one()
        result = False
        if self.name == "/":
            result = True
        return result

    @api.model
    def create(self, values):
        new_values = self._prepare_create_data(values)
        passanger = super(FleetWorkOrderPassanger, self).create(new_values)
        passanger._create_sequence()
        return passanger

    @api.multi
    def copy(self, defaults):
        str_warning = _("You can't copy passanger data")
        raise UserError(str_warning)

    @api.onchange("work_order_id")
    def onchange_start_location_id(self):
        self.start_location_id = False
        if self.work_order_id:
            wo = self.work_order_id
            self.start_location_id = wo.start_location_id

    @api.onchange("work_order_id")
    def onchange_end_location_id(self):
        self.end_location_id = False
        if self.work_order_id:
            wo = self.work_order_id
            self.end_location_id = wo.end_location_id

    @api.onchange("work_order_id")
    def onchange_seat_id(self):
        domain = {
            "seat_id": [
                ("id", "=", 0),
            ],
        }
        obj_seat = self.env["fleet.vehicle.seat"]
        self.seat_id = False
        if self.work_order_id and self.work_order_id.vehicle_id:
            wo = self.work_order_id
            criteria = [
                ("vehicle_id", "=", wo.vehicle_id.id),
            ]
            seat_ids = obj_seat.search(criteria).ids
            domain["seat_id"] = [
                ("id", "in", seat_ids),
            ]
        return {"domain": domain}

    @api.constrains("partner_id", "work_order_id")
    def check_same_partner(self):
        obj_passanger = self.env[self._model]
        if self.partner_id:
            criteria = [
                ("id", "!=", self.id),
                ("partner_id", "!=", False),
                ("partner_id", "=", self.partner_id.id),
            ]
            passanger_count = obj_passanger.search_count(criteria)
            if passanger_count > 0:
                raise ValidationError(_("Duplicate Partner"))
