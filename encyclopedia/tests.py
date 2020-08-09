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
        """Test search. Exact match."""

        c = Client()
        url = '/search/'
        keyword = util.list_entries()[0]
        response = c.post(url, {'keyword': keyword}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML(f'<h1>{keyword}</h1>', str(response.content))

    def test_search_substring(self):
        """Test search. Substring."""

        c = Client()
        url = '/search/'
        keyword = 'py'
        response = c.post(url, {'keyword': keyword}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<li><a href="/wiki/Python">Python</a></li>', str(response.content))

    def test_search_not_found(self):
        """Test search. Not found."""

        c = Client()
        url = '/search/'
        keyword = 'notFound'
        response = c.post(url, {'keyword': keyword}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<h3>Sorry. Entry not found.</h3>', str(response.content))

    def test_random_page(self):
        """Test random page."""

        c = Client()
        url = ('/random_page/')
        response = c.get(url, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        """Test create page."""

        c = Client()
        url = ('/new_page/')
        response = c.get(url, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_create_page_post(self):
        """Test create page. Post request."""

        c = Client()
        response = c.post(
            '/new_page/',
            {'file_name': 'new_entry', 'entry': '*Title'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, os.path.exists('./entries/new_entry.md'))

        os.remove('./entries/new_entry.md')
