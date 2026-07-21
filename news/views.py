from django.shortcuts import redirect
from .models import Subscriber

# Create your views here.
def subscriber_leave(request , subscriber_uuid):
    subscriber = Subscriber.objects.filter(unsubscribe_token=subscriber_uuid)
    if subscriber.exists():
        subscriber.first().delete()

        return redirect("/")