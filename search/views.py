from django.shortcuts import render

from search.utils import get_results


def search(request):
    query = request.GET.get('query', '')

    results = get_results(query)

    data = {
        'query': query,
        'results': results,
        'page': {
            'long_name': 'Search results for %s' % query,
        }
    }

    return render(request, 'search/results.html', data)
