# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProxyBackendDeviceType(models.Model):
    _inherit = "proxy.backend_device_type"

    door_control = fields.Boolean(string="Door Control")
