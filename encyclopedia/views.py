import markdown2
import os

from django.shortcuts import render

from . import util


def index(request):
    """Main page."""

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry_name):
    """Render entry page."""

    with open(f'./entries/{entry_name}.md') as ef:
        entry_file_content = ef.readlines()

        # convert markdown to html
        ef_content_html = markdown2.markdown(''.join(entry_file_content))

    context = {
        'entry_content': ef_content_html
    }
    return render(request, "encyclopedia/entry.html", context)
