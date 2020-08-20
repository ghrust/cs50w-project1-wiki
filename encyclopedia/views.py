import os
import random
import markdown2

from django.shortcuts import render, redirect

from . import util
from .forms import NewPageForm, EditPageForm


def index(request):
    """Main page."""

    context = {
        "entries": util.list_entries()
    }

    return render(request, "encyclopedia/index.html", context)


def entry_page(request, entry_name):
    """Render entry page."""

    # convert markdown to html
    ef_content = util.get_entry(entry_name)
    if ef_content:
        ef_content_html = markdown2.markdown(ef_content)
    else:
        return render(request, 'encyclopedia/404.html', status=404)

    context = {
        'entry_title': entry_name,
        'entry_content': ef_content_html
    }
    return render(request, "encyclopedia/entry.html", context)


def search(request):
    """Search form."""

    keyword = request.GET['keyword']
    if keyword in util.list_entries():
        return redirect('entry_page', entry_name=keyword)
    else:
        context = {
            'search_results': util.search_entry(keyword)
        }
        return render(
            request,
            'encyclopedia/search_results.html',
            context
        )


def random_page(request):
    rand_entry_name = random.choice(util.list_entries())
    return redirect('entry_page', entry_name=rand_entry_name)


def new_page(request):

    if request.method == 'POST':
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            entry = form.cleaned_data.get('entry')

            util.save_entry(title, f'# {title}\n\n{entry}')

            return redirect('entry_page', entry_name=title)
    else:
        form = NewPageForm()

    context = {'form': form}

    return render(request, 'encyclopedia/new_page.html', context)


def edit_page(request, entry_name):

    if request.method == 'POST':
        form = EditPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            entry = form.cleaned_data['entry']

            os.rename(f'./entries/{entry_name}.md', f'./entries/{title}.md')
            util.save_entry(title, f'# {title}\n\n{entry}')

            return redirect('entry_page', entry_name=title)
    else:
        with open(f'./entries/{entry_name}.md') as ef:
            ef_content = ef.readlines()

        data = {
            'title': entry_name,
            'entry': ''.join(ef_content[1:])
        }

        form = EditPageForm(data)

    context = {'form': form}

    return render(request, 'encyclopedia/edit_page.html', context)
