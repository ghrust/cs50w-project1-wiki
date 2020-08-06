from .forms import SearchForm


def search_form(request):
    form = SearchForm()
    return {'search_form': form}
