from django.core.management.base import BaseCommand
from user.models import UserProfile

class Command(BaseCommand):
    help = "Reset all profile scores to 0"

    def handle(self, *args, **options):
        UserProfile.objects.update(score=0)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully reset score for all profiles."
            )
        )