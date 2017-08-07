from django.db import models
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.db.models.signals import post_save


# Create your models here.

class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance) # If self.instance exists, exclude it so that it doesn't display in the followed_by.
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user) # (user_obj, true)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False


class UserProfile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')    # user.profile
    following   = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    # user.profile.following -- users I follow
    # user.follower_by -- users that follow me
    objects = UserProfileManager()	# UserProfile.objects.all()

    def __str__(self):
        return str(self.user.username) + " following " + str(self.following.all().count()) + " people/person."

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user)

    def get_follow_url(self):
        return reverse_lazy("profiles:follow", kwargs={"username":self.user.username})

    def get_absolute_url(self):
        return reverse_lazy("profiles:detail", kwargs={"username":self.user.username})

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)
post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
