from .models import UserProfile

def profile_picture(request):
    if request.user.is_authenticated  :
        profile_id = UserProfile.objects.get(user=request.user).profile_picture
    else:
        profile_id = None

    return {
        'profile_id' : profile_id
    }