# -*- coding: utf-8 -*-
# © 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Vehicle Door Control",
    "version": "8.0.1.2.0",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "category": "Fleet",
    "installable": True,
    "depends": [
        "fleet",
        "proxy_backend"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/proxy_backend_device_type_views.xml",
        "views/vehicle_door_views.xml",
        "views/fleet_vehicle_views.xml"
    ],
}
