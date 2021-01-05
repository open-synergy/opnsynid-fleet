# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


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
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
            %s
            )""" % (
            self._table,
            self._select(),
            self._from(),
            self._where(),
            self._group_by()))
