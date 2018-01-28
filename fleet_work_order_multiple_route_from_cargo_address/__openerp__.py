# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Create Multiple Route From Cargo Address",
    "version": "8.0.1.0.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order_cargo",
        "fleet_work_order_multiple_route",
    ],
    "data": [
        "wizards/create_route_from_cargo.xml",
        "views/fleet_work_order_views.xml",
    ],
}
