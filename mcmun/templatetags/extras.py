from django import template
from mcmun.models import SecretariatMember, Coordinator


register = template.Library()

@register.filter
def get_range(end, start=1):
	"""
	Filter - returns a list containing range made from given value

	"""
	return range(start, end + 1)


@register.inclusion_tag('bio.html')
def get_bios(bio_type, page):
    if bio_type == 'sec':
        person_type = SecretariatMember
    else:
        person_type = Coordinator

    return {
        'bio_type': bio_type,
        'bios': person_type.objects.all(),
        'page': page,
    }
