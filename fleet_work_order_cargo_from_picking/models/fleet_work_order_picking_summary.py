# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, tools
from psycopg2.extensions import AsIs


class FleetWorkOrderPickingSummary(models.Model):
    _name = "fleet.work.order.picking_summary"
    _description = "Fleet Work Order Picking Summary"
    _auto = False

    work_order_id = fields.Many2one(
        string="# Work Order",
        comodel_name="fleet.work.order",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    reserved_availability = fields.Float(
        string="Availability",
    )
    product_uom_id = fields.Many2one(
        string="Product UoM",
        comodel_name="product.uom",
    )

    @api.multi
    def _prepare_criteria_move_ids(self):
        self.ensure_one()
        picking_ids = self.work_order_id.picking_ids.ids
        result = [
            ("picking_id", "in", picking_ids),
            ("product_id", "=", self.product_id.id),
        ]
        return result

    @api.multi
    def _compute_stock_move_ids(self):
        obj_stock_move = self.env["stock.move"]

        for document in self:
            move_ids = obj_stock_move.search(document._prepare_criteria_move_ids())
            document.stock_move_ids = move_ids.ids

    stock_move_ids = fields.Many2many(
        string="Moves",
        comodel_name="stock.move",
        compute="_compute_stock_move_ids",
        store=False,
    )

    def _select(self):
        select_str = """
            SELECT
                row_number() OVER() AS id,
                b.work_order_id AS work_order_id,
                a.product_id AS product_id,
                COALESCE(SUM(c.qty), 0) AS reserved_availability,
                a.product_uom AS product_uom_id
        """
        return select_str

    def _from(self):
        from_str = """
            FROM stock_move AS a
            JOIN stock_picking AS b on a.picking_id=b.id
            LEFT JOIN stock_quant AS c on a.id=c.reservation_id
        """
        return from_str

    def _where(self):
        where_str = """
            WHERE b.work_order_id IS NOT NULL
        """
        return where_str

    def _group_by(self):
        group_by_str = """
            GROUP BY b.work_order_id,a.product_id,a.product_uom
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        view_query = """%s
            %s
            %s
            %s""" % (
            self._select(),
            self._from(),
            self._where(),
            self._group_by(),
        )
        cr.execute(
            "CREATE OR REPLACE VIEW %s AS %s", (AsIs(self._table), AsIs(view_query))
        )
