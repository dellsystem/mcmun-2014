import re

from django.conf import settings
from django.db.models import Q, loading

"""
From: http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
"""


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def get_results(query_string):
    if not query_string:
        return

    all_results = []
    for search_model, search_fields in settings.SEARCH_MODELS:
        model = loading.get_model(*search_model.split('.', 1))
        q = get_query(query_string, search_fields)
        results = model.objects.filter(q)

        # If the model defines an is_searchable method, filter by that
        is_searchable = getattr(model, 'is_searchable', None)
        if callable(is_searchable):
            results = [r for r in results if r.is_searchable()]

        # Otherwise, the model is assumed to be searchable by default
        all_results.extend(results)

    return all_results
