# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.exceptions import Warning as UserError, ValidationError
from openerp.tools.translate import _
import base64
from datetime import datetime
import pytz
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import math


class FleetWorkOrderPassanger(models.Model):
    _name = "fleet.work_order_passanger"
    _inherit = ["mail.thread"]
    _description = "Fleet Work Order Passanger"

    @api.multi
    @api.depends("work_order_id")
    def _compute_allowed_type_ids(self):
        for passanger in self:
            passanger.allowed_type_ids = False
            if passanger.work_order_id and \
                    passanger.work_order_id.type_id and \
                    passanger.work_order_id.type_id.passanger_type_ids:
                result = []
                for pass_type in passanger.work_order_id.\
                        type_id.passanger_type_ids:
                    result.append(pass_type.passanger_type_id.id)
                passanger.allowed_type_ids = [(6, 0, result)]

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
        string="Passanger",
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
            "draft": [
                ("readonly", False),
            ],
        },
        track_visibility="onchange",
    )
    end_location_id = fields.Many2one(
        string="End Location",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
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
    allowed_type_ids = fields.Many2many(
        string="Allowed Type",
        comodel_name="fleet.work_order_passanger_type",
        compute="_compute_allowed_type_ids",
        store=False,
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

    barcode_image = fields.Text(
        string="Barcode image",
        compute="_compute_barcode_image",
    )

    start_time = fields.Char(
        string="Start Time",
        compute="_compute_time"
    )

    end_time = fields.Char(
        string="End Time",
        compute="_compute_time" 
    )

    def ean_checksum(self, eancode):
        if len(eancode) != 13:
            return -1
        oddsum=0
        evensum=0
        total=0
        eanvalue=eancode
        reversevalue = eanvalue[::-1]
        finalean=reversevalue[1:]

        for i in range(len(finalean)):
            if i % 2 == 0:
                oddsum += int(finalean[i])
            else:
                evensum += int(finalean[i])
        total=(oddsum * 3) + evensum

        check = int(10 - math.ceil(total % 10.0)) %10
        return check

    def check_ean(self, eancode):
        if not eancode:
            return True
        if len(eancode) != 13:
            return False
        try:
            int(eancode)
        except:
            return False
        return self.ean_checksum(eancode) == int(eancode[-1])

    @api.multi
    def _convert_datetime_utc(self, dt):
        self.ensure_one()
        user = self.env.user
        convert_dt = datetime.strptime(dt, DEFAULT_SERVER_DATETIME_FORMAT)

        if user.tz:
            tz = pytz.timezone(user.tz)
        else:
            tz = pytz.utc

        convert_utc = pytz.utc.localize(convert_dt).astimezone(tz)
        format_utc = datetime.strftime(
            convert_utc,
            "%H:%M"
        )

        return format_utc

    @api.multi
    @api.depends(
        "work_order_id.date_start",
        "work_order_id.date_end"
    )
    def _compute_time(self):
        for data in self:
            data.start_time = False      
            data.end_time = False
            if data.work_order_id:
                data.start_time =\
                    self._convert_datetime_utc(data.work_order_id.date_start)
                data.end_time =\
                    self._convert_datetime_utc(data.work_order_id.date_end)

    @api.multi
    @api.depends("name")
    def _compute_barcode_image(self):
        for data in self:
            data.barcode_image = None
            if data.name != "/":
                if self.check_ean(data.name):
                    try:
                        barcode = self.env["report"].barcode(
                            "EAN13",
                            data.name,
                            width=300,
                            height=100,
                            humanreadable=0
                        )
                    except (ValueError, AttributeError):
                        raise Warning(_("Cannot convert into barcode."))
                    barcode_base64 = base64.b64encode(barcode)
                    data.barcode_image = "data:image/png;base64," + barcode_base64

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

    @api.onchange("work_order_id")
    def onchange_type_id(self):
        self.type_id = False

    @api.constrains("partner_id", "work_order_id")
    def check_same_partner(self):
        obj_passanger = self.env["fleet.work_order_passanger"]
        if self.partner_id:
            criteria = [
                ("id", "!=", self.id),
                ("partner_id", "!=", False),
                ("partner_id", "=", self.partner_id.id),
            ]
            passanger_count = obj_passanger.search_count(criteria)
            if passanger_count > 0:
                raise ValidationError(_("Duplicate Partner"))
