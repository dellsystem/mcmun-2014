from django.shortcuts import render

from search.utils import get_results


def search(request):
    query = request.GET.get('query', '')

    results = get_results(query)

    data = {
        'query': query,
        'results': results,
    }
    return render(request, 'search/results.html', data)
