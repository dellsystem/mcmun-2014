import csv
import sys

from django.core.management.base import BaseCommand, CommandError

from mcmun.models import RegisteredSchool


class Command(BaseCommand):
    help = ("Lists all the schools for which num_delegates differs from the "
            "number of delegate assignments.")

    def handle(self, *args, **options):
        print "Approved schools: "
        # First check approved schools
        for school in RegisteredSchool.objects.filter(is_approved=True):
            num_assigned = school.get_num_assignments()
            if school.num_delegates != num_assigned:
                print school, school.num_delegates, num_assigned

        # Now check unapproved schools with assignments
        print "Unapproved schools: "
        for school in RegisteredSchool.objects.filter(is_approved=False):
            num_assigned = school.get_num_assignments()
            if num_assigned > 0:
                print school, num_assigned
