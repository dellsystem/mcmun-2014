from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum

from mcmun.models import RegisteredSchool


TEST_SCHOOLS = [1, 2, 3, 28, 35, 36]

class Command(BaseCommand):
    help = 'Shows registration-related statistics.'

    def handle(self, *args, **options):
        schools = RegisteredSchool.objects.all()
        approved_schools = schools.filter(is_approved=True) \
                                  .exclude(id__in=TEST_SCHOOLS)

        num_delegates = approved_schools.aggregate(Sum('num_delegates')) \
                                        ['num_delegates__sum']
        # please forgive me
        amount_owed = sum(map(float, (s.get_total_owed() for s in approved_schools)))
        amount_paid = approved_schools.aggregate(Sum('amount_paid')) \
                                      ['amount_paid__sum']

        self.stdout.write("Total number of schools: %d" % schools.count())
        self.stdout.write("Approved schools: %d" % approved_schools.count())
        self.stdout.write("Number of approved delegates: %d" % num_delegates)
        self.stdout.write("Total amount owed: $%.2f" % amount_owed)
        self.stdout.write("Total amount paid: $%.2f" % amount_paid)
