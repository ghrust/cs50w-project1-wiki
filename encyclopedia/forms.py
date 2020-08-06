import re
from .util import list_entries

from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

    def search_entry(self, keyword):
        result = []
        for entry in list_entries():
            if re.findall(keyword, entry, re.IGNORECASE):
                result.append(entry)

        return result
