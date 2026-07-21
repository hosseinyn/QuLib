from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.conf import settings
from .schema import SubscriberSchema
from .models import Subscriber
from .tasks import send_newsletter_email
from django_ratelimit.decorators import ratelimit

api = NinjaAPI(
    title="News API",
    version="1.0.0",
    docs_url="",
    openapi_url="/openapi.json",
    urls_namespace='newsapi'
)

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == settings.NEWS_API_KEY:
            return {"token": token}
        return None

@api.post("/subscribers")
@ratelimit(key="ip", rate="4/d", block=True)
def add_subscriber(request, payload: SubscriberSchema):  
    try:
        new_subscriber = Subscriber.objects.create(**payload.dict())
        join_message = """ درود! <br>
                    تو از الان عضو خبرنامه کولیب هستی و میتونی اولین نفر از خبر ها و تغییرات در پلتفرم کولیب آگاه بشی."""
        send_newsletter_email.delay("به خبرنامه کولیب خوش اومدی!", join_message, [payload.email] , uuid=new_subscriber.unsubscribe_token)

        return {"message": "success"}
    except:
        return {"message" : "success"}