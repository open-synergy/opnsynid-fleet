# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Multiple Route on Fleet Work Order",
    "version": "8.0.1.1.1",
    "category": "Fleet",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
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
