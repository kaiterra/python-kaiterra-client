"""
Unit tests and integration tests for the Kaiterra API client.
"""
import os
import unittest

_skip_online_tests = os.environ.get(
    'KAITERRA_API_SKIP_ONLINE_TESTS',
    "").lower() in ['true', 't', '1']
skip_online_tests = unittest.skipIf(
    _skip_online_tests,
    "Skipping tests against the live API...")
