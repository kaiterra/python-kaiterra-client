#!/usr/bin/env python3
import json
import unittest
import requests
import requests_mock
from datetime import datetime, timezone
from kaiterra_client import KaiterraAPIClient, Units, AQIStandard


class TestGetSensorData(unittest.TestCase):
    """
    White-box and black-box tests against KaiterraAPIClient using requests_mock
    to provide mock HTTP responses.
    """

    def setUp(self):
        self._client = KaiterraAPIClient(
            api_key='abc123',
            aqi_standard=AQIStandard.USA,
            preferred_units=[Units.DegreesCelsius],
            )

    def test_validate_sensor_ids(self):
        """
        KaiterraAPIClient does some sensor ID validation to save developers time, so make
        sure that works correctly.
        """
        self.assertTrue(self._client._is_valid_sensor_id('/lasereggs/00000000-0001-0001-0000-00007e57c0de'))
        self.assertTrue(self._client._is_valid_sensor_id('/laseregg/00000000-0001-0001-0000-00007e57c0de'))
        self.assertTrue(self._client._is_valid_sensor_id('laseregg/00000000-0001-0001-0000-00007e57c0de'))
        self.assertTrue(self._client._is_valid_sensor_id('lasereggs/0000000000010001000000007e57c0de'))

        self.assertTrue(self._client._is_valid_sensor_id('/sensedges/0000000000010001000000007e57c0de'))
        self.assertTrue(self._client._is_valid_sensor_id('/sensedge/0000000000010001000000007e57c0de'))
        self.assertTrue(self._client._is_valid_sensor_id('sensedges/0000000000010001000000007e57c0de'))
        self.assertTrue(self._client._is_valid_sensor_id('sensedge/0000000000010001000000007e57c0de'))
        self.assertTrue(self._client._is_valid_sensor_id('sensedge/00000000-0001-0001-0000-00007e57c0de'))

        self.assertFalse(self._client._is_valid_sensor_id('thing'))
        self.assertFalse(self._client._is_valid_sensor_id('/thing/0000000000010001000000007e57c0de'))
        self.assertFalse(self._client._is_valid_sensor_id('/lasereggs/0000000-0001-0001-0000-00007e57c0de'))
        self.assertFalse(self._client._is_valid_sensor_id('/lasereggs/g0000000-0001-0001-0000-00007e57c0de'))
        self.assertFalse(self._client._is_valid_sensor_id('/lasereggs/00000000-0001-00-01-0000-00007e57c0de'))

    @requests_mock.mock()
    def test_load(self, m):
        """
        Tests submission and parsing of a simple batch request for a laser egg
        and a sensedge
        """
        m.post('https://api.kaiterra.cn/v1/batch', text='''[{"code":200,"body":"{\\"id\\":\\"00000000-0001-0001-0000-00007e57c0de\\",\\"latest\\":[{\\"param\\":\\"rpm10c\\",\\"units\\":\\"µg/m³\\",\\"span\\":60,\\"points\\":[{\\"ts\\":\\"2019-07-03T09:48:33Z\\",\\"value\\":120.000000,\\"aqi\\":83}]},{\\"param\\":\\"rpm25c\\",\\"units\\":\\"µg/m³\\",\\"span\\":60,\\"points\\":[{\\"ts\\":\\"2019-07-03T09:48:33Z\\",\\"value\\":173.000000,\\"aqi\\":223}]}]}"},{"code":200,"body":"{\\"id\\":\\"00000000-0031-0001-0000-00007e57c0de\\",\\"latest\\":[{\\"param\\":\\"rco2\\",\\"units\\":\\"ppm\\",\\"span\\":60,\\"points\\":[{\\"ts\\":\\"2019-07-03T09:48:33Z\\",\\"value\\":1673.000000,\\"aqi\\":117}]},{\\"param\\":\\"rhumid\\",\\"source\\":\\"km102\\",\\"units\\":\\"%\\",\\"span\\":60,\\"points\\":[{\\"ts\\":\\"2019-07-03T09:48:33Z\\",\\"value\\":67.380000}]},{\\"param\\":\\"rpm10c\\",\\"source\\":\\"km100\\",\\"units\\":\\"µg/m³\\",\\"span\\":60,\\"points\\":[{\\"ts\\":\\"2019-07-03T09:48:33Z\\",\\"value\\":125.000000,\\"aqi\\":86}]},{\\"param\\":\\"rpm25c\\",\\"source\\":\\"km100\\",\\"units\\":\\"µg/m³\\",\\"span\\":60,\\"points\\":[{\\"ts\\":\\"2019-07-03T09:48:33Z\\",\\"value\\":174.000000,\\"aqi\\":224}]},{\\"param\\":\\"rtemp\\",\\"source\\":\\"km102\\",\\"units\\":\\"C\\",\\"span\\":60,\\"points\\":[{\\"ts\\":\\"2019-07-03T09:48:33Z\\",\\"value\\":14.430000}]},{\\"param\\":\\"rtvoc\\",\\"source\\":\\"km102\\",\\"units\\":\\"ppb\\",\\"span\\":60,\\"points\\":[{\\"ts\\":\\"2019-07-03T09:48:33Z\\",\\"value\\":425.500000,\\"aqi\\":142}]}]}"}]''')

        le_id = '/lasereggs/00000000-0001-0001-0000-00007e57c0de'
        se_id = '/sensedges/00000000-0031-0001-0000-00007e57c0de'

        r = self._client.get_latest_sensor_readings([le_id, se_id])

        # Verify the POST request body
        self.assertListEqual(m.request_history[0].json(), [{
            'method': 'GET',
            'relative_url': le_id + '?format=series_major&aqi=us&units=C',
        }, {
            'method': 'GET',
            'relative_url': se_id + '?format=series_major&aqi=us&units=C',
        }])

        self.assertListEqual(r, [
        {
            'rpm10c': {
                'units': Units.MicrogramsPerCubicMeter,
                'points': [{
                    'ts': datetime(2019, 7, 3, 9, 48, 33, tzinfo=timezone.utc),
                    'value': 120.0,
                    'aqi': 83,
                }]
            },
            'rpm25c': {
                'units': Units.MicrogramsPerCubicMeter,
                'points': [{
                    'ts': datetime(2019, 7, 3, 9, 48, 33, tzinfo=timezone.utc),
                    'value': 173.0,
                    'aqi': 223,
                }]
            }
        }, {
            'rco2': {
                'units': Units.PartsPerMillion,
                'points': [{
                    'ts': datetime(2019, 7, 3, 9, 48, 33, tzinfo=timezone.utc),
                    'value': 1673.0,
                    'aqi': 117,
                }]
            },
            'rhumid': {
                'units': Units.Percent,
                'source': 'km102',
                'points': [{
                    'ts': datetime(2019, 7, 3, 9, 48, 33, tzinfo=timezone.utc),
                    'value': 67.38,
                }],
            },
            'rpm10c': {
                'units': Units.MicrogramsPerCubicMeter,
                'source': 'km100',
                'points': [{
                    'ts': datetime(2019, 7, 3, 9, 48, 33, tzinfo=timezone.utc),
                    'value': 125.0,
                    'aqi': 86,
                }]
            },
            'rpm25c': {
                'units': Units.MicrogramsPerCubicMeter,
                'source': 'km100',
                'points': [{
                    'ts': datetime(2019, 7, 3, 9, 48, 33, tzinfo=timezone.utc),
                    'value': 174.0,
                    'aqi': 224,
                }]
            },
            'rtemp': {
                'units': Units.DegreesCelsius,
                'source': 'km102',
                'points': [{
                    'ts': datetime(2019, 7, 3, 9, 48, 33, tzinfo=timezone.utc),
                    'value': 14.43,
                }]
            },
            'rtvoc': {
                'units': Units.PartsPerBillion,
                'source': 'km102',
                'points': [{
                    'ts': datetime(2019, 7, 3, 9, 48, 33, tzinfo=timezone.utc),
                    'value': 425.5,
                    'aqi': 142,
                }]
            }
        }])


if __name__ == '__main__':
    unittest.main()
