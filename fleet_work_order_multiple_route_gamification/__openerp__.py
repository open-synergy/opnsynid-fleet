# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Multiple Route Gamification",
    "version": "8.0.1.0.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "fleet_work_order_gamification",
        "fleet_work_order_multiple_route",
    ],
    "data": [
        "views/fleet_route_template_views.xml",
        "views/fleet_work_order_type_views.xml",
        "views/fleet_work_order_views.xml",
    ],
}
