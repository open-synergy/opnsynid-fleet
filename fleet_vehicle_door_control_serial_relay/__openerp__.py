# -*- coding: utf-8 -*-
# © 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Vehicle Door Control Serial Relay",
    "version": "8.0.1.0.0",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "category": "Fleet",
    "installable": True,
    "depends": [
        "fleet_vehicle_door_control",
        "proxy_backend_serial_relay"
    ],
    "data": [
        "data/proxy_backend_device_type_data.xml",
        "views/vehicle_door_views.xml"
    ],
}
