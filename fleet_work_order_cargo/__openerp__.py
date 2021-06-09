# Copyright 2016 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Work Order Cargo",
    "version": "8.0.2.0.0",
    "category": "Fleet",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order",
        "fleet_vehicle_cargo",
        "stock_shipment_management",
    ],
    "data": [
        "views/fleet_work_order_views.xml",
        "views/shipment_plan_views.xml",
    ],
}
