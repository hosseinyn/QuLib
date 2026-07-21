from django.contrib.admin.models import LogEntry
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Delete all Django admin logs"

    def handle(self, *args, **options):
        table = LogEntry._meta.db_table

        with connection.cursor() as cursor:
            if connection.vendor == "postgresql":
                cursor.execute(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;')
            else:
                LogEntry.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS("Successfully cleared all Django admin logs")
        )