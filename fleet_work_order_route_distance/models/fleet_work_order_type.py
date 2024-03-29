# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp import _, api, models
from openerp.exceptions import Warning as UserError

_logger = logging.getLogger(__name__)
try:
    import googlemaps
except ImportError:
    _logger.debug(
        "Could not import googlemaps. "
        "Please make sure this library is available in "
        "your environment."
    )


class FleetWorkOrderType(models.Model):
    _inherit = "fleet.work.order.type"

    @api.multi
    def _get_auth(self):
        for rec in self:
            keychain = rec.env["keychain.account"]
            retrieve = keychain.retrieve
            accounts = retrieve([["namespace", "=", "google_maps"]])
            return accounts[0]

    @api.multi
    def button_calc_distance(self):
        if self.start_location_id and self.end_location_id:
            keychain_account = self._get_auth()

            data = keychain_account.get_data()

            if data["type"] == "basic":
                try:
                    gmaps = googlemaps.Client(
                        key=keychain_account.get_password(),
                    )
                except Exception as error:
                    raise UserError(
                        _("Your Key is not valid. Please try again.\n %s") % error
                    )
            elif data["type"] == "premium":
                try:
                    gmaps = googlemaps.Client(
                        client_id=keychain_account["login"],
                        client_secret=keychain_account.get_password(),
                    )
                except Exception as error:
                    raise UserError(
                        _("Your Key is not valid. Please try again.\n %s") % error
                    )

            origins = {
                "lat": self.start_location_id.partner_latitude,
                "lng": self.start_location_id.partner_longitude,
            }

            destinations = {
                "lat": self.end_location_id.partner_latitude,
                "lng": self.end_location_id.partner_longitude,
            }
            distance_matrix = gmaps.distance_matrix(
                origins=origins, destinations=destinations
            )
            distance_value = distance_matrix["rows"][0]["elements"][0]["distance"][
                "value"
            ]
            self.distance = distance_value / 1000.0
        else:
            raise UserError(_("Start Location and End Location can't be empty"))
