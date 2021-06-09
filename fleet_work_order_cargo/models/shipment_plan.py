# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ShipmentPlan(models.Model):
    _inherit = "shipment.plan"

    @api.multi
    def _fleet_work_order_group(self, domain, **kwargs):
        obj_wo = self.env["fleet.work.order"]
        criteria = [
            ("state", "in", ["draft", "confirmed"]),
        ]
        wos = obj_wo.search(criteria).name_get()
        return wos, None

    _group_by_full = {
        "fleet_work_order_id": _fleet_work_order_group,
    }

    fleet_work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order",
        readonly=True,
    )
    loading_space = fields.Float(
        string="Loading Space",
        related="fleet_work_order_id.loading_space",
        readonly=True,
        store=True,
    )
    load_capacity = fields.Float(
        string="Load Capacity",
        related="fleet_work_order_id.load_capacity",
        readonly=True,
        store=True,
    )
