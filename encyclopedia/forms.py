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

    title = forms.CharField(
        max_length=100,
        required=True
    )

    entry = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    def clean_title(self):
        """Validate if title exists."""

        title = self.cleaned_data.get('title')
        if title in list_entries():
            raise forms.ValidationError('Name exists. Take another.')

        return title

    def save_entry_to_file(self, title, entry):
        """Save entry to file *.md"""

        with open(f'./entries/{title}.md', 'x') as ef:
            ef.write(f'# {title}\n' + entry)
