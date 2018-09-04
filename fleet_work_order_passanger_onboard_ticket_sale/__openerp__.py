# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Onboard Passanger Ticket Sale",
    "version": "8.0.1.1.1",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order_passanger_ticket_sale",
    ],
    "data": [
        "wizards/passanger_boarding_disembark_views.xml",
        "views/fleet_work_order_type_views.xml",
        "views/fleet_work_order_passanger_views.xml",
    ],
}
