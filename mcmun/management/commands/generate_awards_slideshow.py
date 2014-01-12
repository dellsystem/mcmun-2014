import codecs
from xml.dom import minidom
from xml.etree.ElementTree import tostring

from django.core.management.base import BaseCommand, CommandError

from committees.models import AwardAssignment, Committee


class Command(BaseCommand):
    help = ("Generates the awards slideshow, as a PDF.")
    args = '[path to SVG file]'

    def handle(self, filename, *args, **options):
        # First, get all the committee data
        committees = Committee.objects.filter(is_assignable=True)
        committees_dict = {}
        for committee in committees:
            committees_dict[committee.slug] = committee

        svg_file = open(filename)
        doc = minidom.parse(svg_file)
        for g in doc.lastChild.childNodes:
            if g.nodeName == 'g':
                label = g.getAttribute('inkscape:label')
                if label in committees_dict:
                    committee = committees_dict[label]
                    # Fill in the context dict (for string replacements)
                    awards = committee.awards.order_by('-pk')
                    context = {}
                    for i, award in enumerate(awards):
                        j = i + 1
                        if award.position:
                            delegate_name = award.position.assignment
                            school_name = award.position.school.school_name
                        else:
                            delegate_name = 'Wendy Liu'
                            school_name = 'McGill University'

                        context['award_name_%d' % j] = award.award.name
                        context['delegate_name_%d' % j] = delegate_name
                        context['school_name_%d' % j] = school_name

                    for flowPara in g.getElementsByTagName('flowPara'):
                        text = flowPara.firstChild
                        if text:
                            new_value = text.nodeValue % context
                            text.replaceWholeText(new_value)

        # Save the updated SVG
        output_file = codecs.open('updated_awards.svg', 'w', encoding='utf-8')
        output_file.write(doc.toxml())
