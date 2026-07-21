from django.core.management.base import BaseCommand
from django.db import connection

from axes.models import AccessAttempt, AccessLog

class Command(BaseCommand):
    help = "Truncate all django-axes tables"

    def handle(self, *args, **options):
        tables = [
            AccessAttempt._meta.db_table,
            AccessLog._meta.db_table,
        ]

        with connection.cursor() as cursor:
            cursor.execute(
                f"TRUNCATE TABLE {', '.join(tables)} RESTART IDENTITY CASCADE;"
            )

        self.stdout.write(
            self.style.SUCCESS("All django-axes tables have been truncated")
        )