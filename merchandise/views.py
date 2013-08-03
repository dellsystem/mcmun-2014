from django.shortcuts import render

from merchandise.models import Bundle, Item


def main(request):
    bundles = Bundle.objects.all()
    items = Item.objects.all()

    context = {
        'bundles': bundles,
        'items': items,
        'title': 'Merchandise',
    }
    return render(request, 'merchandise.html', context)
