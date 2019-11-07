# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Work Order - A/R Collection",
    "version": "8.0.1.1.1",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order_multiple_route",
        "account_debt_collection",
    ],
    "data": [
        "wizards/fleet_debt_colletion_create.xml",
        "views/fleet_work_order_views.xml",
    ],
}
