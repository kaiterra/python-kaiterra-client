#!/usr/bin/env python3

import os
import unittest
from kaiterraclient.tests import skip_online_tests
from kaiterraclient import KaiterraAPIClient, Units

@skip_online_tests
class GetSensorDataTests(unittest.TestCase):
    """
    Tests for retrieving sensor data.
    """

    def setUp(self):
        if 'KAITERRA_APIV1_URL_KEY' not in os.environ:
            raise Exception('Missing Kaiterra API key in environment variable KAITERRA_APIV1_URL_KEY')
        api_key = os.environ['KAITERRA_APIV1_URL_KEY']

        self._client = KaiterraAPIClient(api_key=api_key, preferred_units=[Units.DegreesFahrenheit])

    def tearDown(self):
        self._client.close()

    def test_simple(self):
        readings = self._client.get_latest_sensor_readings([
            '/lasereggs/00000000-0001-0001-0000-00007e57c0de',
            '/lasereggs/00000000-ffff-0001-ffff-00007e57c0de',
        ])
        self.assertEqual(2, len(readings))

        # First sensor exists, and should have readings
        self.assertIsNotNone(readings[0])
        self.assertIn('rpm25c', readings[0])
        self.assertIsNone(readings[1])

    def test_validate_sensor_ids(self):
        # Malformed UDID
        with self.assertRaises(ValueError):
            self._client.get_latest_sensor_readings(['/lasereggs/0000000-0001-0001-0000-00007e57c0de'])

        # Should be a list, not a string
        with self.assertRaises(ValueError):
            self._client.get_latest_sensor_readings('/lasereggs/00000000-0001-0001-0000-00007e57c0de')


if __name__ == '__main__':
    unittest.main()
