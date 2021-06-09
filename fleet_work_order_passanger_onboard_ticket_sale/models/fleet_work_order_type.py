# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class WorkOrderTypePassangerType(models.Model):
    _inherit = "fleet.work_order_type_passanger"

    onboard_sale = fields.Boolean(
        string="Onboard Ticket Sale",
    )

    @api.multi
    def onboard_ticket_sale(self):
        self.ensure_one()
        obj_sale = self.env["fleet.work_order_passanger_ticket_sale"]
        obj_passanger = self.env["fleet.work_order_passanger"]

        work_order_id = self._context.get("work_order_id", False)

        sale = obj_sale.create(self._prepare_onboard_ticket_sale_data(work_order_id))
        obj_passanger.create(self._prepare_onboard_passanger(sale))
        sale.action_confirm()
        sale.action_valid()
        return sale.print_ticket()

    @api.multi
    def _prepare_onboard_ticket_sale_data(self, work_order_id):
        self.ensure_one()
        pricelist_id = self._get_onboard_ticket_pricelist_id(work_order_id)
        return {
            "work_order_id": work_order_id,
            "pricelist_id": pricelist_id.id,
        }

    @api.multi
    def _get_onboard_ticket_pricelist_id(self, work_order_id):
        self.ensure_one()
        obj_wo = self.env["fleet.work.order"]
        wo = obj_wo.browse([work_order_id])[0]
        return wo.type_id.default_passanger_pricelist_id or False

    @api.multi
    def _prepare_onboard_passanger(self, ticket_sale):
        self.ensure_one()
        wo = ticket_sale.work_order_id
        return {
            "work_order_id": wo.id,
            "pricelist_id": ticket_sale.pricelist_id.id,
            "type_id": self.passanger_type_id.id,
            "product_id": self.product_id.id,
            "price_unit": self._get_price_unit(ticket_sale),
            "order_id": ticket_sale.id,
        }

    @api.multi
    def _get_price_unit(self, ticket_sale):
        self.ensure_one()
        return ticket_sale.pricelist_id.price_get(prod_id=self.product_id.id, qty=1.0)[
            ticket_sale.pricelist_id.id
        ]
