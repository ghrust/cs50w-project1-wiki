import os
import markdown2

from django.test import TestCase

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

    def test_entry_page(self):
        """Test entry page."""

        for entry in util.list_entries():
            url = f'/wiki/{entry}'

            resp = self.client.get(url)

            with open(f'./entries/{entry}.md') as ef:
                entry_file_content = ef.readlines()
                ef_content_html = markdown2.markdown(''.join(entry_file_content))

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(ef_content_html, resp.context['entry_content'])
