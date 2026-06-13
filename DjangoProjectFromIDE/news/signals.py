from django.db.models.signals import post_save
from django.dispatch import receiver
from django_eventstream import send_event
from .models import News

@receiver(post_save, sender=News)
def send_news_update(sender, instance, created, **kwargs):
    if created:
        send_event('news-feed', 'message', {'text': f'Нова новина: {instance.title}'})
