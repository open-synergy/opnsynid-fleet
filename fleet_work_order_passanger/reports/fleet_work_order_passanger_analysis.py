# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class FleetWorkOrderPassangerAnalysis(models.Model):
    _name = "fleet.work_order_passanger_analysis"
    _description = "Fleet Work Order Passanger Analysis"
    _auto = False

    partner_id = fields.Many2one(
        string="Passanger",
        comodel_name="res.partner",
    )
    passanger_type_id = fields.Many2one(
        string="Passanger Type",
        comodel_name="fleet.work_order_passanger_type",
    )
    work_order_type_id = fields.Many2one(
        string="Work Order Type",
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
    date_start = fields.Datetime(
        string="ETD",
    )
    date_end = fields.Datetime(
        string="ETA",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Validation"),
            ("valid", "Valid"),
            ("boarding", "Boarding"),
            ("disembarking", "Disembarking"),
            ("cancel", "Cancel"),
        ],
    )

    def _select(self):
        select_str = """
             SELECT row_number() OVER() as id,
            a.type_id AS passanger_type_id,
            a.partner_id AS partner_id,
            b.type_id AS work_order_type_id,
            b.vehicle_id AS vehicle_id,
            b.driver_id AS driver_id,
            b.date_start AS date_start,
            b.date_end AS date_end,
            a.state AS state
        """
        return select_str

    def _from(self):
        from_str = """
                fleet_work_order_passanger AS a
        """
        return from_str

    def _where(self):
        where_str = """
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN    fleet_work_order AS b ON a.work_order_id = b.id
        """
        return join_str

    def _group_by(self):
        group_str = """
            GROUP BY    a.type_id,
                        a.partner_id,
                        b.type_id,
                        b.vehicle_id,
                        b.driver_id,
                        b.date_start,
                        b.date_end,
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
