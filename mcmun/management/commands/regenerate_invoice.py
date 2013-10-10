from django.core.management.base import BaseCommand, CommandError

from mcmun.models import RegisteredSchool


class Command(BaseCommand):
    help = 'Re-sends the invoice for the school with the supplied pk.'

    def handle(self, *args, **options):
        pk = raw_input('Enter the primary key of the school: ')
        try:
            school = RegisteredSchool.objects.get(pk=pk)
        except RegisteredSchool.DoesNotExist:
           raise CommandError('School with ID %s does not exist!' % pk)

        if not school.is_approved:
            raise CommandError('%s has not been approved yet.' % school)

        confirm = raw_input('School found: %s. Type y to confirm: ' % school)
        if confirm == 'y':
            account = school.account
            school.account = None
            account.delete()
            school.save()
            self.stdout.write('Invoice regenerated and sent for %s.' % school)
        else:
            self.stdout.write('Regeneration cancelled.')
