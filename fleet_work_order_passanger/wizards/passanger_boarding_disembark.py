# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


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
                warning.update({
                    "action": self._reload_action(),
                })

        return {"warning": warning}

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
