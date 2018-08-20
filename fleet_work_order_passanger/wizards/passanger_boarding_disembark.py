# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class PassangerBoardingDisembark(models.TransientModel):
    _name = "fleet.passanger_boarding_disembark"
    _description = "Passanger Boarding/Disembark"

    work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order"
    )

    @api.model
    def _default_device_id(self):
        result = False
        obj_fleet_work_order =\
            self.env["fleet.work.order"]
        work_order_id = self._context.get('default_work_order_id', False)

        if work_order_id:

            criteria = [
                ("id", "=", work_order_id)
            ]

            work_order =\
                obj_fleet_work_order.search(criteria)
            if work_order:
                vehicle = work_order.vehicle_id
            if vehicle:
                door = vehicle.door_ids[0]
                if door:
                    raspberry_relay =\
                        door.raspberry_relay_id
                    if raspberry_relay:
                        result =\
                            raspberry_relay.device_id
        return result

    passanger_code = fields.Char(
        string="# Passanger",
        default=False,
    )
    device_raspberry_id = fields.Many2one(
        string="# Device",
        comodel_name="proxy.backend_device",
        default=_default_device_id
    )

    @api.model
    def _default_channel(self):
        result = False
        obj_fleet_work_order =\
            self.env["fleet.work.order"]
        work_order_id = self._context.get('default_work_order_id', False)

        if work_order_id:

            criteria = [
                ("id", "=", work_order_id)
            ]

            work_order =\
                obj_fleet_work_order.search(criteria)
            if work_order:
                vehicle = work_order.vehicle_id
            if vehicle:
                door = vehicle.door_ids[0]
                if door:
                    raspberry_relay =\
                        door.raspberry_relay_id
                    if raspberry_relay:
                        result =\
                            raspberry_relay.pin
        return result

    channel = fields.Integer(
        string="Channel",
        default=_default_channel
    )

    @api.onchange("passanger_code")
    def onchange_passanger(self):
        obj_passanger = self.env["fleet.work_order_passanger"]
        warning = {}
        domain = []
        if self.passanger_code:
            domain = self._prepare_domain()
            passangers = obj_passanger.search(domain)
            if len(passangers) == 1:
                warning = {
                    "title": "A",
                    "message": "B"
                }
                passanger = passangers[0]
                if passanger.state in ["valid", "disembarking"]:
                    passanger.action_boarding()
                elif passanger.state == "boarding":
                    passanger.action_disembarking()
                self.passanger_code = ""
                warning.update({
                    "action": self._open_door_gpio(),
                })
            else:
                self.passanger_code = ""

        return {"warning": warning}

    @api.multi
    def _open_door_gpio(self):
        self.ensure_one()
        action = self.env.ref(
            "proxy_backend_gpio."
            "proxy_backend_raspberry_relay_on_off_timer_action")
        context = {
            "device_id": self.device_raspberry_id.id,
            "pin": self.channel,
            "interval": 1
        }
        result = action.read()[0]
        result.update({"context": context})
        return result

    @api.multi
    def _reload_action(self):
        self.ensure_one()
        wiz = self.env.ref(
            "fleet_work_order_passanger."
            "fleet_passanger_boarding_disembark_action")
        return wiz.read()[0]

    @api.multi
    def _prepare_domain(self):
        self.ensure_one()
        return [
            ("name", "=", self.passanger_code),
            ("work_order_id", "=", self.work_order_id.id)
        ]

    @api.multi
    def action_clear_barcode(self):
        self.ensure_one()
        self.passanger_barcode = False
        return self._reload_action()
