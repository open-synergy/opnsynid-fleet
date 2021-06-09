# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Management - Picking Wave for Cargo Loading",
    "version": "8.0.2.0.0",
    "category": "Fleet",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
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
