from .models import UserProfile, Badge
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from user.repositories.user_profile_repository import create_user_profile

@receiver(pre_save, sender=UserProfile)
def track_old_score(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_obj = UserProfile.objects.get(pk=instance.pk)
            instance._old_score = old_obj.score
        except UserProfile.DoesNotExist:
            instance._old_score = None
    else:
        instance._old_score = None


@receiver(post_save, sender=UserProfile)
def handle_score_change(sender, instance, created, **kwargs):
    if created:
        return

    old_score = getattr(instance, '_old_score', None)
    new_score = instance.score

    if old_score == new_score:
        return

    badge_name = None
    badge_description = None

    if 5 <= new_score < 15:
        badge_name = "استارتر"
        badge_description = "شروع طوفانی در کولیب با پنج امتیاز"
        
    elif 15 <= new_score < 30:
        badge_name = "لول دو"
        badge_description = "کاربر حرفه ای لول 2 با پانزده امتیاز"
        
    elif new_score >= 30:
        badge_name = "لجندری"
        badge_description = "کاربر لجندری با 30 امتیاز"

    if badge_name:
        Badge.objects.get_or_create(
            user=instance.user,
            name=badge_name,
            defaults={"description": badge_description}
        )


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        create_user_profile(instance, "نامشخص", "نامشخص")