from django.conf import settings
from .models import News, Subscribes
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save


@receiver(post_save, sender=News)
def send_email_to_subscribers(sender, instance, created, **kwargs):
    if created: # only send email for new posts
        subject = f"BONG.UZda Yangilik"
        message = f"Title: {instance.title}\n\n\n\n{instance.subtitle}"
        from_email = settings.EMAIL_HOST_USER
        to_email = Subscribes.objects.values_list('email', flat=True) # get all subscriber emails
        send_mail(subject, message, from_email, to_email, fail_silently=False)