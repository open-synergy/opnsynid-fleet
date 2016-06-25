# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Manage vehicle seat number",
    "version": "8.0.1.0.0",
    "category": "Fleet",
    "website": "https://opensynergy-indonesia.com/",
    "author": "Andhitia Rama,OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "fleet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_vehicle_views.xml",
    ],
    "demo": [
        "demo/fleet_vehicle_demo.xml",
    ],
}
