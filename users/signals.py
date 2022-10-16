from email import message
from pickle import TRUE
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from users.views import profile
from .models import Profile

#@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username = user.username,
            email = user.email,
            name = user.first_name

        )
        subject = f'Hey, ya. Welcome to Skymoders'
        message = 'We are glade you are here! Give 5-_-'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def updateUser(sender, instance, created,**kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()



def profileDelet(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
    print('Deleted', (sender, instance))


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(profileDelet, sender=Profile)
