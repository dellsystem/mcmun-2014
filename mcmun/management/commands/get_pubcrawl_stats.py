from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum

from mcmun.models import RegisteredSchool


TEST_SCHOOLS = [1, 2, 3, 28, 35, 36]

class Command(BaseCommand):
    help = 'Shows pub-crawl related statistics.'

    def handle(self, *args, **options):
        schools = RegisteredSchool.objects.filter(pub_crawl_final=True) \
                                          .exclude(id__in=TEST_SCHOOLS) \
                                          .order_by('email')

        total = schools.aggregate(Sum('num_pub_crawl'))['num_pub_crawl__sum']

        self.stdout.write("Total number registered: %d" % total)
        self.stdout.write("===========================")
        for school in schools:
            if school.num_pub_crawl > 0:
                row = ["%s" % school.school_name,
                    school.email,
                    str(school.num_pub_crawl),
                    school.get_pub_crawl_total_owed()
                ]
                self.stdout.write(','.join(row))
