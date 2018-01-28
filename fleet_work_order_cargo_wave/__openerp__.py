# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Management - Picking Wave for Cargo Loading",
    "version": "8.0.2.0.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order_cargo",
        "stock_picking_wave",
    ],
    "data": [
        "wizards/load_wave_to_cargo.xml",
        "views/fleet_work_order_views.xml",
    ],
}
