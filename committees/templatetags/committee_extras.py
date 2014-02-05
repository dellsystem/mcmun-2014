from django import template

from committees.models import Committee


register = template.Library()


@register.inclusion_tag('awards.html')
def show_awards():
    committees = Committee.objects.filter(is_assignable=True)
    return {
        'committees': committees,
    }
