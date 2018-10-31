# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Fleet Work Order Cargo From Picking",
    "version": "8.0.1.0.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order_cargo",
    ],
    "data": [
        "wizards/load_picking_to_cargo.xml",
        "views/fleet_work_order_type_views.xml",
        "views/fleet_work_order_views.xml",
    ],
}
