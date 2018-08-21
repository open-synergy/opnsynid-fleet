# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Passanger Ticket Sale",
    "version": "8.0.1.1.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order_passanger",
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/product_pricelist_type_data.xml",
        "reports/fleet_work_order_passanger_analysis.xml",
        "views/fleet_work_order_passanger_views.xml",
        "views/fleet_work_order_type_views.xml",
        "views/fleet_work_order_passanger_ticket_sale_views.xml",
        "views/fleet_work_order_views.xml",
    ],
}
