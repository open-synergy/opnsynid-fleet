# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp.tests.common import TransactionCase
from openerp.tools.config import config

_logger = logging.getLogger(__name__)

try:
    from cryptography.fernet import Fernet
except ImportError as err:
    _logger.debug(err)


class BaseFleetWorkOrderRouteDistance(TransactionCase):
    def setUp(self):
        super(BaseFleetWorkOrderRouteDistance, self).setUp()
        # Objects
        self.keychain = self.env["keychain.account"]
        self.order_obj = self.env["fleet.work.order"]

        # Data
        config["keychain_key"] = Fernet.generate_key()

    def _create_account(self):
        vals = {
            "name": "Test Account",
            "namespace": "google_maps",
            "technical_name": "API",
        }
        return self.keychain.create(vals)
