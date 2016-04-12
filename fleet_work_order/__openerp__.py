# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Work Order",
    "version": "8.0.2.0.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        "fleet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "wizard/work_order_depart_views.xml",
        "wizard/work_order_arrive_views.xml",
        "views/fleet_work_order_views.xml",
    ],
    "demo": [
        "demo/res_partner_demo.xml",
        "demo/fleet_demo.xml",
    ],
}
