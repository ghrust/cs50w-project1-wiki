import os

from django.test import Client, TestCase
from . import util

# Create your tests here.
class EncyclopediaTestCase(TestCase):
    """Tests for encyclopedia app"""

    def test_util_list_entries(self):
        """Test util.list_entries()"""
        dir = 'entries/'
        entries_files_count = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
        self.assertEqual(len(util.list_entries()), entries_files_count)

    def test_index(self):
        """Test index page."""
        resp = self.client.get('/')

        self.assertEqual(resp.status_code, 200)
        for entry in util.list_entries():
            self.assertIn(entry, str(resp.content))
