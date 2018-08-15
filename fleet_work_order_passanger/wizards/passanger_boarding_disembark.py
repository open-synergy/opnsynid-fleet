# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields
import requests
import json


class PassangerBoardingDisembark(models.TransientModel):
    _name = "fleet.passanger_boarding_disembark"
    _description = "Passanger Boarding/Disembark"

    passanger_code = fields.Char(
        string="# Passanger",
        default=False,
    )

    @api.onchange("passanger_code")
    def onchange_passanger(self):
        obj_passanger = self.env["fleet.work_order_passanger"]
        warning = {
        }
        if self.passanger_code:
            domain = self._prepare_domain()
            passangers = obj_passanger.search(domain)
            if len(passangers) == 1:
                warning = {
                    "title": "A",
                    "message": "B",
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

        return {"warning": warning}

    @api.multi
    def _json_rpi_gpio_out_on_off_timer(self):
        self.ensure_one()
        result = False
        params = {
            "channel":40,
            "interval":1
        }
        payload = {'params': params}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            'http://192.168.8.108:8069/hw_proxy/rpi_gpio_out_on_off_timer',
            data = json.dumps(payload),
            headers=headers
        )
        return True

    @api.multi
    def _open_door_gpio(self):
        self.ensure_one()
        obj_ir_model_data =\
            self.env["ir.model.data"]
        action = self.env.ref(
            "proxy_backend_gpio."
            "proxy_backend_raspberry_relay_on_off_timer_action")
        context = {
            "device_id": 1,
            "pin": 40,
            "interval": 1
        }
        result = action.read()[0]
        result.update({"context":context})
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
        ]

    @api.multi
    def action_clear_barcode(self):
        self.ensure_one()
        self.passanger_barcode = False
        return self._reload_action()
