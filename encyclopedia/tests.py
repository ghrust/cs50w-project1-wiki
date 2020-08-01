import os
import markdown2

from django.test import TestCase, Client
from selenium import webdriver

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

    def test_entry_page(self):
        """Test entry page."""

        for entry in util.list_entries():
            url = f'/wiki/{entry}'

            resp = self.client.get(url)

            with open(f'./entries/{entry}.md') as ef:
                ef_content = ef.readlines()
                ef_content_html = markdown2.markdown(''.join(ef_content))

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(ef_content_html, resp.context['entry_content'])


# views uses selenium
# class EncyclopediaFrontTestCase(TestCase):
#     """Test front with Selenium."""

#     def setUp(self):
#         self.driver = webdriver.Chrome()

#     # def tearDown(self):
#     #     self.driver.quit()

#     def test_index_selenium(self):
#         self.driver.get('http://0.0.0.0:8000')
#         self.assertIn('http://0.0.0.0:8000', self.driver.current_url)

#     def test_entry_page_content_selenium(self):
#         """Test entry page content."""

#         entry_name = util.list_entries()[0]
#         self.driver.get(f'http://0.0.0.0:8000/wiki/{entry_name}')

#         title = self.driver.find_element_by_tag_name('h1').text

#         self.assertEqual(title, entry_name)
