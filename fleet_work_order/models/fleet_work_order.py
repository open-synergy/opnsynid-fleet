# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class FleetWorkOrder(models.Model):
    _name = "fleet.work.order"
    _description = "Fleet Work Order"
    _inherit = ["mail.thread"]

    name = fields.Char(
        string="# Order",
        required=True,
        readonly=False,
        default="/",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="fleet.work.order.type",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
        required=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "confirmed": [("readonly", False)],
            "depart": [("required", True)],
        },
    )
    driver_id = fields.Many2one(
        string="Driver",
        comodel_name="res.partner",
        required=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "confirmed": [("readonly", False)],
            "depart": [("required", True)],
        },
    )
    co_driver_id = fields.Many2one(
        string="Co-Driver",
        comodel_name="res.partner",
        required=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "confirmed": [("readonly", False)],
        },
    )
    date_start = fields.Datetime(
        string="ETD",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    date_end = fields.Datetime(
        string="ETA",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    real_date_depart = fields.Datetime(
        string="RTD",
        readonly=True,
    )
    real_date_arrive = fields.Datetime(
        string="RTA",
        readonly=True,
    )
    start_odometer = fields.Float(
        string="Starting Odoometer",
    )
    end_odometer = fields.Float(
        string="Ending Odometer",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain="[('customer','=',True)]",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    start_location_id = fields.Many2one(
        string="Start Location",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    end_location_id = fields.Many2one(
        string="End Location",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    distance = fields.Float(
        string="Distance",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    note = fields.Text(
        string="Additional Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("depart", "Depart"),
            ("arrive", "Arrive"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        readonly=True,
        default="draft",
    )

    @api.multi
    def button_confirm(self):
        for order in self:
            order._action_confirm()

    @api.multi
    def button_depart(self):
        for order in self:
            order._action_depart(fields.Datetime.now(),
                                 order.start_odometer)

    @api.multi
    def button_arrive(self):
        for order in self:
            order._action_arrive(fields.Datetime.now(),
                                 order.end_odometer)

    @api.multi
    def button_cancel(self):
        for order in self:
            order._action_cancel()

    @api.multi
    def button_restart(self):
        for order in self:
            order._action_restart()

    @api.constrains(
        "state",
        "vehicle_id",
        "driver_id"
    )
    def _check_vehicle_driver(self):
        if self.state == "depart":
            if not self.vehicle_id or \
                    not self.driver_id:
                raise UserError(_("Warning!"), _(
                    "Vehicle and driver required"))

    @api.onchange(
        "vehicle_id"
    )
    def onchange_vehicle_id(self):
        self.driver_id = False
        if self.vehicle_id:
            self.driver_id = self.vehicle_id.driver_id

    @api.onchange(
        "type_id"
    )
    def onchange_vehicle_id(self):
        self.vehicle_id = False
        if self.type_id:
            wo_type = self.type_id
            self.vehicle_id = wo_type.vehicle_id and \
                wo_type.vehicle_id.id or False

    @api.onchange(
        "type_id"
    )
    def onchange_driver_id(self):
        self.driver_id = False
        if self.type_id:
            wo_type = self.type_id
            self.driver_id = wo_type.driver_id and \
                wo_type.driver_id.id or False

    @api.onchange(
        "type_id"
    )
    def onchange_co_driver_id(self):
        self.co_driver_id = False
        if self.type_id:
            wo_type = self.type_id
            self.co_driver_id = wo_type.co_driver_id and \
                wo_type.co_driver_id.id or False

    @api.onchange(
        "type_id"
    )
    def onchange_start_location_id(self):
        if self.type_id:
            wo_type = self.type_id
            self.start_location_id = wo_type.start_location_id and \
                wo_type.start_location_id.id or False

    @api.onchange(
        "type_id"
    )
    def onchange_end_location_id(self):
        if self.type_id:
            wo_type = self.type_id
            self.end_location_id = wo_type.end_location_id and \
                wo_type.end_location_id.id or False

    @api.onchange(
        "type_id"
    )
    def onchange_distance(self):
        if self.type_id:
            wo_type = self.type_id
            self.distance = wo_type.distance

    @api.multi
    def _action_confirm(self):
        self.ensure_one()
        self.write(self._prepare_confirm_data())

    @api.multi
    def _action_depart(self,
                       date_depart=fields.Datetime.now(),
                       starting_odometer=0.0):
        self.ensure_one()

        self.write(self._prepare_depart_data(date_depart,
                                             starting_odometer))

    @api.multi
    def _action_arrive(self,
                       date_arrive=fields.Datetime.now(),
                       ending_odometer=0.0):
        self.ensure_one()
        self.write(self._prepare_arrive_data(date_arrive,
                                             ending_odometer))

    @api.multi
    def _action_cancel(self):
        self.ensure_one()
        self.write(self._prepare_cancel_data())

    @api.multi
    def _action_restart(self):
        self.ensure_one()
        self.write(self._prepare_restart_data())

    @api.model
    def create(self, vals):
        if vals.get("name", "/") == "/":
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "fleet.work.order") or "/"
        return super(FleetWorkOrder, self).create(vals)

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirmed"
        }

    @api.multi
    def _prepare_depart_data(self, date_depart, starting_odometer):
        self.ensure_one()
        return {
            "state": "depart",
            "real_date_depart": date_depart,
            "start_odometer": starting_odometer,
        }

    @api.multi
    def _prepare_arrive_data(self, date_arrive, ending_odometer):
        self.ensure_one()
        return {
            "state": "arrive",
            "real_date_arrive": date_arrive,
            "end_odometer": ending_odometer,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancelled",
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }


class WorkOrderType(models.Model):
    _name = "fleet.work.order.type"
    _description = "Work Order Type"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
    )
    driver_id = fields.Many2one(
        string="Driver",
        comodel_name="res.partner",
    )
    co_driver_id = fields.Many2one(
        string="Co-Driver",
        comodel_name="res.partner",
    )
    start_location_id = fields.Many2one(
        string="Start Location",
        comodel_name="res.partner",
    )
    end_location_id = fields.Many2one(
        string="End Location",
        comodel_name="res.partner",
    )
    distance = fields.Float(
        string="Distance",
    )
