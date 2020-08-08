import random
import markdown2

from django.shortcuts import render, redirect

from . import util
from .forms import SearchForm


def index(request):
    """Main page."""

    context = {
        "entries": util.list_entries()
    }

    return render(request, "encyclopedia/index.html", context)


def entry_page(request, entry_name):
    """Render entry page."""

    try:
        with open(f'./entries/{entry_name}.md') as ef:
            ef_content = ef.readlines()
    except FileNotFoundError as error:
        print(f'ERROR: {error}')
        return render(request, 'encyclopedia/404.html', status=404)

    # convert markdown to html
    ef_content_html = markdown2.markdown(''.join(ef_content))

    context = {
        'entry_title': entry_name,
        'entry_content': ef_content_html
    }
    return render(request, "encyclopedia/entry.html", context)


def search(request):
    """Search form."""

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            keyword = form.cleaned_data['keyword']

            if keyword in util.list_entries():
                return redirect('entry_page', entry_name=keyword)
            else:
                context = {
                    'search_results': form.search_entry(keyword)
                }
                return render(request, 'encyclopedia/search_results.html', context)

    return redirect('index')


def random_page(request):
    rand_entry_name = random.choice(util.list_entries())
    return redirect('entry_page', entry_name=rand_entry_name)
