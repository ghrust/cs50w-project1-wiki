import markdown2
import os

from django.shortcuts import render

from . import util


def index(request):
    """Main page."""

    context = {
        "entries": util.list_entries()
    }

    return render(request, "encyclopedia/index.html", context)


def entry_page(request, entry_name):
    """Render entry page."""

    with open(f'./entries/{entry_name}.md') as ef:
        ef_content = ef.readlines()

        # convert markdown to html
        ef_content_html = markdown2.markdown(''.join(ef_content))

    context = {
        'entry_title': entry_name,
        'entry_content': ef_content_html
    }
    return render(request, "encyclopedia/entry.html", context)
