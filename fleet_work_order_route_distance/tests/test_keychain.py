# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .base import BaseFleetWorkOrderRouteDistance
from openerp.exceptions import ValidationError


class TestKeyChain(BaseFleetWorkOrderRouteDistance):

    def test_google_maps_validation_data(self):
        account = self._create_account()
        value_data = ("{'type':'wrong'}")

        for value in value_data:
            with self.assertRaises(ValidationError) as err:
                account.write({"data": value})
                self.assertTrue(
                    False,
                    'Should not validate baddly formatted json')
            self.assertTrue(
                'Data should be a valid JSON' in str(err.exception),
                'It should raise a ValidationError')
