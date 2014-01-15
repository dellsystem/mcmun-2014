import csv
import sys

from django.core.management.base import BaseCommand, CommandError

from committees.models import DelegateAssignment as D


class Command(BaseCommand):
    help = ("Exports the delegate name list as a CSV file. For badges.")

    def handle(self, *args, **options):
        csv_writer = csv.writer(open('badges.csv', 'wb'))
        csv_writer.writerow(['id', 'name', 'school', 'committee', 'character'])
        delegates = D.objects.filter(delegate_name__isnull=False).order_by('id')

        for i, d in enumerate(delegates):
            data = [
                str(d.id),
                d.delegate_name,
                d.committee_assignment.school.school_name,
                d.committee_assignment.committee.name,
                d.committee_assignment.assignment,
            ]
            csv_writer.writerow(map(lambda s: s.encode('utf-8'), data))

        print i
