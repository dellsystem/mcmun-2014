import csv
import sys

from django.core.management.base import BaseCommand, CommandError

from committees.models import Committee, CommitteeAssignment
from mcmun.models import RegisteredSchool


class Command(BaseCommand):
    help = ("Imports stuff")

    def handle(self, filepath, **options):
        file = open(filepath)
        committee = Committee.objects.get(slug='itu')
        reader = csv.reader(file, quotechar='"')

        for row in reader:
            positions = row[:2] # entries 0 and 1
            schools = row[2:] # entries 2 and 3

            for position, school_name in zip(positions, schools):
                print position, school_name
                school = RegisteredSchool.objects.get(school_name=school_name)
                school.committeeassignment_set.create(
                    committee=committee,
                    assignment=position,
                    num_delegates=1
                )
