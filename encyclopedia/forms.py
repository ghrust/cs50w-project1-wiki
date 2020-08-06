import re
from .util import list_entries

from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(required=True)

    def search_entry(self, keyword):
        result = []
        for entry in list_entries():
            if re.findall(keyword, entry, re.IGNORECASE):
                result.append(entry)

        return result
