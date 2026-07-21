from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .tasks import send_newsletter_email
from .models import Subscriber
from django.db.models import F

@receiver(post_save, sender=News)
def new_news(sender, instance, created, **kwargs):
    if not created:
        return

    subscribers = Subscriber.objects.values(
        "email",
        "unsubscribe_token",
    )

    for subscriber in subscribers:
        send_newsletter_email.delay(
            subject=instance.subject,
            message=instance.message,
            recipient_list=[subscriber["email"]],
            uuid=subscriber["unsubscribe_token"],
        )