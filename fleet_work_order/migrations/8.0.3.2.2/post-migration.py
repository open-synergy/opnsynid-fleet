# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.api import Environment


def migrate(cr, version):
    if not version:
        return

    env = Environment(cr, SUPERUSER_ID, {})
    obj_order = env["fleet.work.order"]
    sequence_obj = env["ir.sequence"]
    order_ids = obj_order.search([("name", "=", "/")])
    for order in order_ids:
        name = sequence_obj.next_by_code("fleet.work.order")
        table = "fleet_work_order"
        query = """SET name = '%s'
            WHERE id = %d;""" % (
            name,
            order,
        )
        cr.execute("UPDATE %s %s", (table, query))
