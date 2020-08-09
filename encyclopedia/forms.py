import re
from .util import list_entries

from django import forms


class SearchForm(forms.Form):
    """Search form."""

    keyword = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

    def search_entry(self, keyword):
        result = []
        for entry in list_entries():
            if re.findall(keyword, entry, re.IGNORECASE):
                result.append(entry)

        return result


class NewPageForm(forms.Form):
    """Form to create new page."""

    title = forms.CharField(required=True)
    entry = forms.CharField(required=True)

    def save_entry_to_file(self, title, entry):
        try:
            with open(f'./entries/{title}.md', 'x') as ef:
                ef.write(f'# {title}\n' + entry)
        except FileExistsError as e:
            print(e)
