
import unittest
from utils import is_good_response, request_data

#to test run python3.6 -m unittest

class UtilsTests(unittest.TestCase):
    def test_is_good_response(self):
        self.assertFalse(is_good_response(None))

    def test_request_data(self):
        self.assertIsNotNone(request_data('https://randomuser.me/api/'))
        self.assertIsNone(request_data(''))
