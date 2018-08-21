# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Passanger Manifest",
    "version": "8.0.1.4.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order",
        "fleet_vehicle_seat_number",
        "web_onchange_action",
        "fleet_vehicle_door_control_raspberry_relay"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "menu.xml",
        "wizards/passanger_boarding_disembark_views.xml",
        "reports/fleet_work_order_passanger_analysis.xml",
        "views/fleet_work_order_passanger_type_views.xml",
        "views/fleet_work_order_views.xml",
        "views/fleet_work_order_type_views.xml",
        "views/fleet_work_order_passanger_views.xml",
    ],
}
