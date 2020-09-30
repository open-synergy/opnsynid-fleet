# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Fleet Work Order Cargo From Picking",
    "version": "8.0.2.1.0",
    "category": "Fleet",
    "website": "https://simetri-sinergi.id/",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order_cargo",
        "stock_picking_measurement",
    ],
    "data": [
        "wizards/load_picking_to_cargo.xml",
        "views/fleet_work_order_type_views.xml",
        "views/fleet_work_order_views.xml",
        "views/stock_picking_views.xml",
    ],
}
