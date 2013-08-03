from django.shortcuts import render
from cms.models import Page


def main(request, name='home'):
    try:
        page = Page.objects.get(short_name=name)
    except Page.DoesNotExist:
        return render(request, '404.html')

    context = {
        'page': page,
        'title': page.long_name,
    }

    return render(request, 'page.html', context)
