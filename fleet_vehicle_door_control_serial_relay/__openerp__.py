# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Vehicle Door Control Serial Relay",
    "version": "8.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "category": "Fleet",
    "installable": True,
    "depends": ["fleet_vehicle_door_control", "proxy_backend_serial_relay"],
    "data": ["data/proxy_backend_device_type_data.xml", "views/vehicle_door_views.xml"],
}
