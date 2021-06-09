# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CreateRouteFromCargo(models.TransientModel):
    _name = "fleet.create_route_from_cargo"
    _description = "Create Route From Cargo"

    @api.model
    def _default_line_ids(self):
        wo_id = self.env.context.get("active_id")
        obj_wo = self.env["fleet.work.order"]
        wo = obj_wo.browse([wo_id])[0]
        result = []
        num = 0
        for cargo in wo.cargo_ids:
            num += 1
            result.append(
                (
                    0,
                    0,
                    {
                        "sequence": num,
                        "destination_address_id": cargo.to_address_id.id,
                    },
                )
            )
        return result

    @api.model
    def _default_work_order_id(self):
        wo_id = self.env.context.get("active_id")
        obj_wo = self.env["fleet.work.order"]
        wo = obj_wo.browse([wo_id])[0]
        return wo

    work_order_id = fields.Many2one(
        string="Work Order",
        comodel_name="fleet.work.order",
        required=True,
        default=lambda self: self._default_work_order_id(),
    )
    start_address_id = fields.Many2one(
        string="Starting Address",
        comodel_name="res.partner",
        required=True,
    )
    end_address_id = fields.Many2one(
        string="Ending Address",
        comodel_name="res.partner",
        required=True,
    )
    line_ids = fields.One2many(
        string="Destination",
        comodel_name="fleet.create_route_from_cargo_line",
        inverse_name="wizard_id",
        default=lambda self: self._default_line_ids(),
    )

    @api.multi
    def action_create_route(self):
        for wiz in self:
            wiz._create_route()

    @api.multi
    def _create_route(self):
        self.ensure_one()
        obj_route = self.env["fleet.route"]
        wo = self.work_order_id
        wo.route_ids.unlink()
        num = 0
        for line in self.line_ids:
            if num == 0:
                start_name = self.start_address_id.name
                start_address_id = self.start_address_id.id
            else:
                start_name = self.line_ids[num - 1].destination_address_id.name
                start_address_id = self.line_ids[num - 1].destination_address_id.id

            end_name = line.destination_address_id.name
            end_address_id = line.destination_address_id.id

            route_name = "{} - {}".format(start_name, end_name)

            data = {
                "order_id": wo.id,
                "name": route_name,
                "start_location_id": start_address_id,
                "end_location_id": end_address_id,
            }
            obj_route.create(data)
            num += 1

        start_name = self.line_ids[num - 1].destination_address_id.name
        start_address_id = self.line_ids[num - 1].destination_address_id.id
        end_name = self.end_address_id.name
        end_address_id = self.end_address_id.id
        route_name = "{} - {}".format(start_name, end_name)

        data = {
            "order_id": wo.id,
            "name": route_name,
            "start_location_id": start_address_id,
            "end_location_id": end_address_id,
        }
        obj_route.create(data)
        wo.write(
            {
                "multiple_route": True,
            }
        )


class CreateRouteFromCargoLines(models.TransientModel):
    _name = "fleet.create_route_from_cargo_line"
    _description = "Create Route From Cargo Lines"
    _order = "wizard_id, sequence"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="fleet.create_route_from_cargo",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
    )
    destination_address_id = fields.Many2one(
        string="Destinantion",
        comodel_name="res.partner",
        required=True,
    )
