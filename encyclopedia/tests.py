import os
import markdown2

from django.test import TestCase, Client

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

        c = Client()
        response = c.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(util.list_entries(), response.context['entries'])
        for entry in util.list_entries():
            self.assertInHTML(f'<a href="/wiki/{entry}">{entry}</a>', str(response.content))

    def test_entry_page(self):
        """Test entry page."""

        c = Client()

        for entry in util.list_entries():
            url = f'/wiki/{entry}'

            response = c.get(url)

            with open(f'./entries/{entry}.md') as ef:
                ef_content = ef.readlines()
                ef_content_html = markdown2.markdown(''.join(ef_content))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(ef_content_html, response.context['entry_content'])
            self.assertInHTML(f'<h1>{entry}</h1>', str(response.content))

    def test_error_entry_not_found(self):
        """Test if file for requested entry is not found."""

        c = Client()
        url = '/wiki/file_not_found'
        response = c.get(url)

        self.assertEqual(response.status_code, 404)

    def test_search_exact_match(self):
        """Test for search feature. Exact match."""

        c = Client()
        url = '/search/'
        keyword = util.list_entries()[0]
        response = c.post(url, {'keyword': keyword}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML(f'<h1>{keyword}</h1>', str(response.content))
