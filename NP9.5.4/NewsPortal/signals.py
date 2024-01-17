from django.conf import settings
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import PostCategory, Post, Author
from django.utils import timezone
from datetime import date

def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview[:20]+"...",
            'link': f'{settings.SITE_URL}newsportal/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body=preview,
        from_email='uvedomleniynewsportal@ya.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()

#@receiver(m2m_changed, sender=PostCategory)
#def notify_about_new_post(sender, instance, **kwargs):
#    if kwargs['action'] == 'post_add':
#        categories = instance.posts_mtm.all()
#        subscribers_emails = []
#
#       for cat in categories:
#            subscribers = cat.subscribers.all()
#            subscribers_emails += [s.email for s in subscribers]
#
#        send_notifications(instance.preview(), instance.pk, instance.heading, subscribers_emails)

@receiver(m2m_changed, sender=PostCategory)
def every_week_message(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.posts_mtm.all()
        subscribers_emails = []
        for cat in categories:
            subscribers_emails += cat.subscribers.all()

        subscribers_emails = [s.email for s in subscribers_emails]

        send_notifications(instance.preview(), instance.pk, instance.heading, subscribers_emails)