from collections import defaultdict
from operator import itemgetter

from django.core.management.base import BaseCommand, CommandError

from committees.models import AwardAssignment, Committee
from mcmun.models import RegisteredSchool as S


def get_highest_value(d):
    # Sort the dictionary by value and return the top entry's key
    return sorted(d.items(), key=itemgetter(1))[0][0]


class Command(BaseCommand):
    help = ("Calculates the best small and large delegations.")

    def handle(self, *args, **options):
        award_points = {
            'Best Delegate': 5,
            'Outstanding Delegate': 4,
            'Honorable Mention': 3,
            'Book Award': 1,
        }

        # Calculate the points, and the number of winners, for each school
        school_points = defaultdict(int)
        school_winners = defaultdict(int)
        for award in AwardAssignment.objects.filter(position__isnull=False):
            num_points = award_points[award.award.name]
            school = award.position.school
            school_points[school.school_name] += num_points
            school_winners[school.school_name] += 1

        # Figure out the totals for each school
        small_totals = {}
        large_totals = {}
        for school_name in school_points:
            num_points = school_points[school_name]
            num_winners = school_winners[school_name]
            num_delegates = S.objects.get(school_name=school_name).num_delegates
            total = (num_points + num_winners) / float(num_delegates)

            print school_name,
            print "%d points, %d winners, %d delegates; %.2f total" % (
                num_points, num_winners, num_delegates, total)

            if 2 <= num_delegates <= 15:
                small_totals[school_name] = total
                print "small delegation"
            elif num_delegates >= 16:
                large_totals[school_name] = total
                print "large delegation"

        # Sort them by value
        best_large = get_highest_value(large_totals)
        best_small = get_highest_value(small_totals)

        print "Best large delegation: ",
        print best_large

        print "Best small delegation: ",
        print best_small

        # Relation between NGOs and voting? How do I know what an NGO is
