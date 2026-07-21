from django.core.management.base import BaseCommand
from logs.models import UserAccessLog

class Command(BaseCommand):
    help = "Reset all user access logs"

    def handle(self, *args, **options):
        UserAccessLog.objects.delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully reset all logs"
            )
        )