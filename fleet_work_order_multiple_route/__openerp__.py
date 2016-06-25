# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Multiple Route on Fleet Work Order",
    "version": "8.0.1.0.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com/",
    "author": "Andhitia Rama, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "fleet_work_order",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_route_template_views.xml",
        "views/fleet_work_order_views.xml",
        "views/fleet_work_order_type_views.xml",
    ],
    "demo": [
        "demo/fleet_route_template_demo.xml",
    ],
}
