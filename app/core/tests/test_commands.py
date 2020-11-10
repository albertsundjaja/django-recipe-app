from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTestCase(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        # mock the connect method
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # provide return value for the mocked method
            gi.return_value = True
            call_command('wait_for_db')
            # we can then check the mock method is being called once
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=None)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # here we are providing the return value differently after 6 times
            # this works like a generator function, the first 5 is an OperationalError while the 6th one returns true
            # side effect allows us to raise exception as well as return value
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)