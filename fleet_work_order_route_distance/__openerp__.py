# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Work Order Route Distance",
    "version": "8.0.1.1.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "fleet_work_order",
        "base_geolocalize",
        "keychain"
    ],
    "external_dependencies": {
        "python": [
            "googlemaps",
        ],
    },
    "data": [
        "views/fleet_work_order_views.xml",
        "views/fleet_work_order_type_views.xml"
    ],
}
