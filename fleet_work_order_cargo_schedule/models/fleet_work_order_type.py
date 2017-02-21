# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta
from openerp import models, fields, api
from openerp.tools.translate import _


class FleetWorkOrderType(models.Model):
    _inherit = "fleet.work.order.type"

    cargo_schedule_ids = fields.One2many(
        string="Schedules",
        comodel_name="fleet.work.order.cargo.schedule",
        inverse_name="fleet_work_order_type_id",
    )

    @api.multi
    def action_add_schedule(self):
        for order_type in self:
            self._add_schedule()

    @api.multi
    def _add_schedule(self):
        self.ensure_one()
        obj_schedule = self.env[
            "fleet.work.order.cargo.schedule"]
        obj_cron = self.env[
            "ir.cron"]
        schedule = obj_schedule.create({
            "fleet_work_order_type_id": self.id,
        })
        name = _("Work Order Cargo Schedule: %s" % self.name)
        args = "[%s]" % (str(schedule.id))
        cron = obj_cron.create({
            "name": name,
            "user_id": self.env.user.id,
            "active": False,
            "model": "fleet.work.order.cargo.schedule",
            "function": "run_schedule",
            "args": args,
        })
        schedule.cron_id = cron


class FleetWorkOrderCargoSchedule(models.Model):
    _name = "fleet.work.order.cargo.schedule"
    _description = "Fleet Work Order Cargo Schedule"

    fleet_work_order_type_id = fields.Many2one(
        string="Fleet Work Order Type",
        comodel_name="fleet.work.order.type",
        ondelete="cascade",
    )
    name = fields.Char(
        string="Schedule Name",
        related="cron_id.name",
    )
    cron_id = fields.Many2one(
        string="Cron Job",
        comodel_name="ir.cron",
        ondelete="restrict",
    )
    interval_number = fields.Integer(
        string="Repeat every x",
        related="cron_id.interval_number",
    )
    interval_type = fields.Selection(
        string="Interval Unit",
        selection=[
            ("hours", "Hours"),
            ("work_days", "Work Days"),
            ("days", "Days"),
            ("weeks", "Weeks"),
            ("months", "Months"),
        ],
        related="cron_id.interval_type",
    )
    numbercall = fields.Integer(
        string="Number of Calls",
        related="cron_id.numbercall",
    )
    nextcall = fields.Datetime(
        string="Next Execution Date",
        related="cron_id.nextcall",
    )
    cron_active = fields.Boolean(
        string="Active",
        related="cron_id.active",
    )
    start_offset = fields.Float(
        string="Offset",
        default=0.0,
    )

    @api.multi
    def unlink(self):
        for schedule in self:
            cron = schedule.cron_id
            schedule.cron_id = False
            cron.unlink()
        super(FleetWorkOrderCargoSchedule, self).unlink()

    @api.model
    def run_schedule(self, schedule_id):
        schedule = self.browse(schedule_id)
        obj_order = self.env[
            "fleet.work.order"]
        date_start = datetime.now() + timedelta(hours=+schedule.start_offset)
        order = obj_order.create({
            "type_id": schedule.fleet_work_order_type_id.id,
            "date_start": date_start,
            "date_end": date_start,
        })
        order.onchange_type_id()
