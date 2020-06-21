from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_read(self):
        """Test waiting for db when db is available"""
        # if throws OperationalError then database is not available
        # otherwise database is available
        # patch will MOCK the below string module
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            # wait for db is the management command we create
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # side affect will be used from DjangoMock
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
