# Copyright 2019 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Work Order Gamification",
    "version": "8.0.1.0.0",
    "category": "Fleet",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order",
        "gamification",
    ],
    "data": [
        "views/fleet_work_order_type_views.xml",
        "views/fleet_work_order_views.xml",
    ],
}
