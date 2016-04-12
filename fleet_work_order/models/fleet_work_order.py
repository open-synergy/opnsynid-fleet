# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import except_orm


class FleetWorkOrder(models.Model):
    _name = "fleet.work.order"
    _description = "Fleet Work Order"
    _inherit = ["mail.thread"]

    @api.one
    @api.depends("passanger_manifest_ids.state")
    def _compute_passanger(self):
        self.passanger_count_boarding = 0
        self.passanger_count_no_show = 0
        self.passanger_count_cancel = 0
        self.passanger_count_estimation = 0
        self.passanger_count_waiting = 0
        self.passanger_count_confirm = 0
        for passanger in self.passanger_manifest_ids:
            if passanger.state == "boarding":
                self.passanger_count_boarding += 1
                self.passanger_count_estimation += 1
            elif passanger.state == "no_show":
                self.passanger_count_no_show += 1
            elif passanger.state == "cancelled":
                self.passanger_count_cancel += 1
            elif passanger.state == "draft":
                self.passanger_count_estimation += 1
                self.passanger_count_waiting += 1
            elif passanger.state == "confirmed":
                self.passanger_count_estimation += 1
                self.passanger_count_confirm += 1

    @api.one
    @api.depends("route_ids")
    def _compute_route(self):
        self.start_location_id = False
        self.end_location_id = False
        self.distance = 0.0
        if self.route_ids:
            self.start_location_id = self.route_ids[0].start_location_id.id
            self.end_location_id = self.route_ids[
                len(self.route_ids) - 1].end_location_id.id
            for route in self.route_ids:
                self.distance += route.distance

    name = fields.Char(
        string="# Order",
        required=True,
        readonly=True,
        default="/",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="fleet.work.order.type",
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
    )
    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
        required=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)],
            'depart': [('required', True)],
        },
    )
    max_passanger = fields.Integer(
        string="Max. Passanger",
        )
        
    driver_id = fields.Many2one(
        string="Driver",
        comodel_name="res.partner",
        required=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)],
            'depart': [('required', True)],
        },
    )
    co_driver_id = fields.Many2one(
        string="Co-Driver",
        comodel_name="res.partner",
        required=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)],
        },
    )
    date_start = fields.Datetime(
        string="Date Start",
        required=True,
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
    )
    date_end = fields.Datetime(
        string="Date End",
        required=True,
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
    )
    real_date_depart = fields.Datetime(
        string="Real Depart Time",
        readonly=True,
        )
    real_date_arrive = fields.Datetime(
        string="Real Arrive Time",
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
            'draft': [('readonly', False)],
        },
    )
    passanger_count = fields.Integer(
        string="Passanger Count",
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)],
        },
    )
    passanger_manifest = fields.Boolean(
        string="Require Passanger Manifest",
        default=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
    )
    passanger_manifest_ids = fields.One2many(
        string="Passanger Manifest",
        comodel_name="fleet.passanger.manifest",
        inverse_name="order_id",
        readonly=True,
    )
    passanger_count_estimation = fields.Integer(
        string="Num. Estimation",
        store=True,
        readonly=True,
        compute="_compute_passanger",
    )
    passanger_count_confirm = fields.Integer(
        string="Num. Confirm",
        store=True,
        readonly=True,
        compute="_compute_passanger",
    )
    passanger_count_boarding = fields.Integer(
        string="Num. Boarding",
        store=True,
        readonly=True,
        compute="_compute_passanger",
    )
    passanger_count_no_show = fields.Integer(
        string="Num. No Show",
        store=True,
        readonly=True,
        compute="_compute_passanger",
    )
    passanger_count_cancel = fields.Integer(
        string="Num. Cancel",
        store=True,
        readonly=True,
        compute="_compute_passanger",
    )
    passanger_count_waiting = fields.Integer(
        string="Num. Waiting Confirmation",
        store=True,
        readonly=True,
        compute="_compute_passanger",
    )
    route_ids = fields.One2many(
        string="Routes",
        comodel_name="fleet.route",
        inverse_name="order_id",
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
    )
    start_location_id = fields.Many2one(
        string="Start Location",
        store=True,
        comodel_name="res.partner",
        readonly=True,
        compute="_compute_route",
    )
    end_location_id = fields.Many2one(
        string="End Location",
        store=True,
        comodel_name="res.partner",
        readonly=True,
        compute="_compute_route",
    )
    distance = fields.Float(
        string="Distance",
        store=True,
        readonly=True,
        compute="_compute_route",
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
            order._action_confirm(self)

    @api.multi
    def button_depart(self):
        for order in self:
            order._action_depart(self, 
                fields.Datetime.now(),
                order.start_odometer)

    @api.multi
    def button_arrive(self):
        for order in self:
            order._action_arrive(self,
                fields.Datetime.now(),
                order.end_odometer)

    @api.multi
    def button_cancel(self):
        for order in self:
            order._action_cancel(self)

    @api.multi
    def button_restart(self):
        for order in self:
            order._action_restart(self)

    @api.one
    @api.constrains("state", "vehicle_id", "driver_id")
    def _check_vehicle_driver(self):
        if self.state == "depart":
            if not self.vehicle_id or \
                    not self.driver_id:
                raise except_orm(_("Warning!"), _(
                "Vehicle and driver required"))


    @api.onchange("vehicle_id")
    def onchange_vehicle_id(self):
        self.driver_id = False
        self.max_passanger = 0
        if self.vehicle_id:
            self.driver_id = self.vehicle_id.driver_id
            self.max_passanger = self.vehicle_id.seats
        

    @api.onchange('type_id')
    def onchange_type_id(self):
        self.vehicle_id = False
        self.driver_id = False
        self.co_driver_id = False
        self.passanger_manifest = False
        self.route_ids.unlink()
        if self.type_id:
            wo_type = self.type_id
            self.vehicle_id = wo_type.vehicle_id and \
                wo_type.vehicle_id.id or False
            self.driver_id = wo_type.driver_id and \
                wo_type.driver_id.id or False
            self.co_driver_id = wo_type.co_driver_id and \
                wo_type.co_driver_id.id or False
            self.passanger_manifest = wo_type.passanger_manifest
            if wo_type.route_ids:
                routes = []
                for route in wo_type.route_ids:
                    res = {
                        'name': route.name,
                        'sequence': route.sequence,
                        'route_template_id': route.route_template_id.id,
                        'start_location_id': route.start_location_id.id,
                        'end_location_id': route.end_location_id.id,
                        'distance': route.distance,
                        }
                    routes.append((0,0,res))
                self.route_ids = routes
                    


    @api.model
    def _action_confirm(self, order):
        self.ensure_one()
        order.write(self._prepare_confirm_data(order))

    @api.model
    def _action_depart(self, order,
            date_depart=fields.Datetime.now(),
            starting_odometer=0.0):
        self.ensure_one()
        if not order._check_passanger_count(order):
            raise except_orm(_("Invalid passanger count"), _(
                "Passanger count is not equal with passanger manifest"))

        order.write(self._prepare_depart_data(order,
            date_depart, starting_odometer))

    @api.model
    def _action_arrive(self, order,
            date_arrive=fields.Datetime.now(),
            ending_odometer=0.0):
        self.ensure_one()
        order.write(self._prepare_arrive_data(order,
            date_arrive, ending_odometer))

    @api.model
    def _action_cancel(self, order):
        self.ensure_one()
        order.write(self._prepare_cancel_data(order))

    @api.model
    def _action_restart(self, order):
        self.ensure_one()
        order.write(self._prepare_restart_data(order))

    @api.model
    def _prepare_confirm_data(self, order):
        self.ensure_one()
        return {
            'name': self._create_sequence(order),
            'state': 'confirmed',
        }

    @api.model
    def _prepare_depart_data(self, order, date_depart, starting_odometer):
        self.ensure_one()
        return {
            'state': 'depart',
            'real_date_depart': date_depart,
            'start_odometer': starting_odometer,
        }

    @api.model
    def _prepare_arrive_data(self, order, date_arrive, ending_odometer):
        self.ensure_one()
        return {
            'state': 'arrive',
            'real_date_arrive': date_arrive,
            'end_odometer': ending_odometer,
        }

    @api.model
    def _prepare_cancel_data(self, order):
        self.ensure_one()
        return {
            'state': 'cancelled',
        }

    @api.model
    def _prepare_restart_data(self, order):
        self.ensure_one()
        return {
            'state': 'draft',
        }

    @api.model
    def _create_sequence(self, order):
        self.ensure_one()
        if order.name == '/':
            name = self.env['ir.sequence'].get('fleet.work.order')
        else:
            name = order.name
        return name

    @api.model
    def _check_passanger_count(self, order):
        result = True
        if order.passanger_manifest and \
                order.passanger_count_boarding != order.passanger_count:
            result = False
        return result


class FleetRouteTemplate(models.Model):
    _name = "fleet.route.template"
    _description = "Fleet's Route Template"

    name = fields.Char(
        string="Name",
        required=True,
        readonly=False,
    )
    start_location_id = fields.Many2one(
        string="From",
        comodel_name="res.partner",
        required=True,
    )
    end_location_id = fields.Many2one(
        string="To",
        comodel_name="res.partner",
        required=True,
    )
    distance = fields.Float(
        string="Distance",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )


class FleetRoute(models.Model):
    _name = "fleet.route"
    _description = "Fleet Route"
    _order = "sequence"

    name = fields.Char(
        string="Route",
        required=True,
    )
    order_id = fields.Many2one(
        string="# Order",
        comodel_name="fleet.work.order",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
    )
    route_template_id = fields.Many2one(
        string="Route Template",
        comodel_name="fleet.route.template",
        required=True,
    )
    start_location_id = fields.Many2one(
        string="From",
        comodel_name="res.partner",
        required=True,
    )
    end_location_id = fields.Many2one(
        string="To",
        comodel_name="res.partner",
        required=True,
    )
    distance = fields.Float(
        string="Distance",
    )

    @api.onchange("route_template_id")
    def onchange_route_template_id(self):
        if self.route_template_id:
            route_template = self.route_template_id
            self.start_location_id = route_template.start_location_id.id
            self.end_location_id = route_template.end_location_id.id
            self.distance = route_template.distance
        else:
            self.start_location_id = False
            self.end_location_id = False
            self.distance = 0.0


class FleetPassangerManifest(models.Model):
    _name = "fleet.passanger.manifest"
    _description = "Fleet Passanger Manifest"
    _inherit = ["mail.thread"]

    name = fields.Char(
        string="# Passanger",
        required=True,
        readonly=True,
        default="/",
    )
    order_id = fields.Many2one(
        string="# Order",
        comodel_name="fleet.work.order",
        required=True,
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
        domain=[("state", '=', "confirmed")],
    )
    date_start = fields.Datetime(
        string="Depart",
        related="order_id.date_start",
        store=True,
    )
    date_end = fields.Datetime(
        string="Arrive",
        related="order_id.date_end",
        store=True,
    )
    start_location_id = fields.Many2one(
        string="From",
        comodel_name="res.partner",
        related="order_id.start_location_id",
        store=True,
    )
    end_location_id = fields.Many2one(
        string="To",
        comodel_name="res.partner",
        related="order_id.end_location_id",
        store=True,
    )
    partner_id = fields.Many2one(
        string="Passanger",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
        domain=[
            ("is_company","=",False),
            ],
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("boarding", "Boarding"),
            ("no_show", "No Show"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        readonly=True,
        default="draft",
    )

    @api.multi
    def button_confirm(self):
        for order in self:
            order._action_confirm(self)

    @api.multi
    def button_boarding(self):
        for order in self:
            order._action_boarding(self)

    @api.multi
    def button_no_show(self):
        for order in self:
            order._action_no_show(self)

    @api.multi
    def button_cancel(self):
        for order in self:
            order._action_cancel(self)

    @api.multi
    def button_restart(self):
        for order in self:
            order._action_restart(self)

    @api.model
    def _action_confirm(self, order):
        self.ensure_one()
        order.write(self._prepare_confirm_data(order))

    @api.model
    def _action_boarding(self, order):
        self.ensure_one()
        order.write(self._prepare_boarding_data(order))

    @api.model
    def _action_no_show(self, order):
        self.ensure_one()
        order.write(self._prepare_no_show_data(order))

    @api.model
    def _action_cancel(self, order):
        self.ensure_one()
        order.write(self._prepare_cancel_data(order))

    @api.model
    def _action_restart(self, order):
        self.ensure_one()
        order.write(self._prepare_restart_data(order))

    @api.model
    def _prepare_confirm_data(self, passanger):
        self.ensure_one()
        name = self._create_sequence(passanger)
        return {
            "name": name,
            "state": "confirmed",
        }

    @api.model
    def _prepare_boarding_data(self, passanger):
        self.ensure_one()
        return {
            "state": "boarding",
        }

    @api.model
    def _prepare_cancel_data(self, passanger):
        self.ensure_one()
        return {
            "state": "cancelled",
        }

    @api.model
    def _prepare_no_show_data(self, passanger):
        self.ensure_one()
        return {
            "state": "no_show",
        }

    @api.model
    def _prepare_restart_data(self, passanger):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.model
    def _create_sequence(self, passanger):
        self.ensure_one()
        if passanger.name == '/':
            name = self.env['ir.sequence'].get('fleet.passanger.manifest')
        else:
            name = passanger.name
        return name

class WorkOrderType(models.Model):
    _name = 'fleet.work.order.type'
    _description = 'Work Order Type'

    @api.one
    @api.depends("route_ids")
    def _compute_route(self):
        self.start_location_id = False
        self.end_location_id = False
        self.distance = 0.0
        if self.route_ids:
            self.start_location_id = self.route_ids[0].start_location_id.id
            self.end_location_id = self.route_ids[
                len(self.route_ids) - 1].end_location_id.id
            for route in self.route_ids:
                self.distance += route.distance

    name = fields.Char(
        string='Name',
        required=True,
        )
    code = fields.Char(
        string='Code',
        required=True,
        )
    active = fields.Boolean(
        string='Active',
        default=True,
        )
    passanger_manifest = fields.Boolean(
        string='Required Passanger Manifest',
        )
    vehicle_id = fields.Many2one(
        string='Vehicle',
        comodel_name='fleet.vehicle',
        )
    driver_id = fields.Many2one(
        string='Driver',
        comodel_name='res.partner',
        )
    co_driver_id = fields.Many2one(
        string='Co-Driver',
        comodel_name='res.partner',
        )
    route_ids = fields.One2many(
        string='Routes',
        comodel_name='fleet.work.order.type.route',
        inverse_name='type_id',
        )
    start_location_id = fields.Many2one(
        string="Start Location",
        store=True,
        comodel_name="res.partner",
        readonly=True,
        compute="_compute_route",
    )
    end_location_id = fields.Many2one(
        string="End Location",
        store=True,
        comodel_name="res.partner",
        readonly=True,
        compute="_compute_route",
    )
    distance = fields.Float(
        string="Distance",
        store=True,
        readonly=True,
        compute="_compute_route",
    )

class WorkOrderTypeRoute(models.Model):
    _description = 'Work Order Type Route'
    _name = 'fleet.work.order.type.route'


    name = fields.Char(
        string='Name',
        required=True,
        )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        )
    type_id = fields.Many2one(
        string='Work Order Type',
        comodel_name='fleet.work.order.type',
        )
    route_template_id = fields.Many2one(
        comodel_name="fleet.route.template",
        string="Route Template",
        )
    start_location_id = fields.Many2one(
        string='From',
        comodel_name='res.partner',
        )
    end_location_id = fields.Many2one(
        string='To',
        comodel_name='res.partner',
        )
    distance = fields.Float(
        string="Distance",
        )

    @api.onchange('route_template_id')
    def onchange_route_template(self):
        if self.route_template_id:
            template = self.route_template_id
            self.sequence = template.sequence
            self.start_location_id = template.start_location_id.id
            self.end_location_id = template.end_location_id.id
            self.distance = template.distance

