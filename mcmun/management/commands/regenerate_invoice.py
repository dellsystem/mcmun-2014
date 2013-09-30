from django.core.management.base import BaseCommand, CommandError

from mcmun.models import RegisteredSchool


class Command(BaseCommand):
    help = 'Re-sends the invoice for the school with the supplied pk.'

    def handle(self, pk, *args, **options):
        try:
            school = RegisteredSchool.objects.get(pk=pk)
        except RegisteredSchool.DoesNotExist:
           raise CommandError('School with ID %s does not exist!' % pk)

        if not school.is_approved:
            raise CommandError('%s has not been approved yet.' % school)

        account = school.account
        school.account = None
        account.delete()
        school.save()
        self.stdout.write('Invoice regenerated and sent for %s.' % school)
