# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class FleetWorkOrderAnalysis(models.Model):
    _name = "fleet.work_order_analysis"
    _description = "Fleet Work Order Analysis"
    _auto = False

    type_id = fields.Many2one(
        string="Type",
        comodel_name="fleet.work.order.type",
    )
    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
    )
    driver_id = fields.Many2one(
        string="Driver",
        comodel_name="res.partner",
    )
    co_driver_id = fields.Many2one(
        string="Co-Driver",
        comodel_name="res.partner",
    )
    date_start = fields.Datetime(
        string="ETD",
    )
    date_end = fields.Datetime(
        string="ETA",
    )
    real_date_depart = fields.Datetime(
        string="RTD",
    )
    real_date_arrive = fields.Datetime(
        string="RTA",
    )
    odometer = fields.Float(
        string="Odoometer",
    )
    start_location_id = fields.Many2one(
        string="Start Location",
        comodel_name="res.partner",
    )
    end_location_id = fields.Many2one(
        string="End Location",
        comodel_name="res.partner",
    )
    distance = fields.Float(
        string="Distance",
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
    )

    def _select(self):
        select_str = """
             SELECT row_number() OVER() as id,
             a.type_id AS type_id,
             a.vehicle_id AS vehicle_id,
             a.driver_id AS driver_id,
             a.co_driver_id AS co_driver_id,
             a.date_start AS date_start,
             a.date_end AS date_end,
             a.real_date_depart AS real_date_depart,
             a.real_date_arrive AS real_date_arrive,
             a.start_location_id AS start_location_id,
             a.end_location_id AS end_location_id,
             a.state AS state,
             SUM(a.end_odometer - a.start_odometer) AS odometer,
             SUM(a.distance) AS distance
        """
        return select_str

    def _from(self):
        from_str = """
                fleet_work_order AS a
        """
        return from_str

    def _where(self):
        where_str = """
        """
        return where_str

    def _join(self):
        join_str = """
        """
        return join_str

    def _group_by(self):
        group_str = """
            GROUP BY    a.type_id,
                        a.vehicle_id,
                        a.driver_id,
                        a.co_driver_id,
                        a.date_start,
                        a.date_end,
                        a.real_date_depart,
                        a.real_date_arrive,
                        a.start_location_id,
                        a.end_location_id,
                        a.state
        """
        return group_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where(),
            self._group_by()
        ))
