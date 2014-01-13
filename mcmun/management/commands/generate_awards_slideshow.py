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

                # Chop off the number and ! at the end to get the committee name
                # This is a really hacky workaround to using a regex
                if label.endswith('!'):
                    committee_name = label[:-2]
                else:
                    # Don't need to change anything, it's not a committee
                    continue

                if committee_name in committees_dict:
                    committee = committees_dict[committee_name]
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
