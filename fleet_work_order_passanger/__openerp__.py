# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Passanger Manifest",
    "version": "8.0.1.7.2",
    "category": "Fleet",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order",
        "fleet_vehicle_seat_number",
        "web_onchange_action",
        "fleet_vehicle_door_control_raspberry_relay",
        "hr",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/ir_actions_server_data.xml",
        "menu.xml",
        "wizards/passanger_boarding_disembark_views.xml",
        "reports/fleet_work_order_passanger_analysis.xml",
        "views/fleet_work_order_passanger_type_views.xml",
        "views/fleet_work_order_views.xml",
        "views/fleet_work_order_type_views.xml",
        "views/fleet_work_order_passanger_views.xml",
    ],
}
