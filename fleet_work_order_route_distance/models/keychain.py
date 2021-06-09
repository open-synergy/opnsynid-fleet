# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class GoogleMapsAccount(models.Model):
    _inherit = "keychain.account"

    namespace = fields.Selection(selection_add=[("google_maps", "Google Maps")])

    def _google_maps_init_data(self):
        return {"type": "basic"}

    def _google_maps_validate_data(self, data):
        if data.get("type") not in ["basic", "premium"]:
            return False
        return True
