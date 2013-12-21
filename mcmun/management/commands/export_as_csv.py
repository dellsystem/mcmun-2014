"""
 Prints a CSV of all fields of a model.
"""
import csv
import sys

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model


class Command(BaseCommand):
    help = ("Output the specified model as CSV")
    args = '[appname.ModelName]'

    def handle(self, *app_labels, **options):
        app_name, model_name = app_labels[0].split('.')
        model = get_model(app_name, model_name)
        field_names = [f.name for f in model._meta.fields]
        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
        writer.writerow(field_names)
        for instance in model.objects.all():
            writer.writerow([unicode(getattr(instance, f)).encode('utf-8') for f in field_names])
