from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
from .models import Post, Category


@shared_task
def every_monday_message():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    this_week_posts = Post.objects.filter(time_create__gt=last_week)
    for cat in Category.objects.all():
        post_list = this_week_posts.filter(posts_mtm=cat)
        if post_list:
            subs = cat.subscribers.values('username', 'email')
            recipients = []
            for subscriber in subs:
                recipients.append(subscriber['email'])

            html_content = render_to_string(
                'everyweek.html',
                {
                    'link': f'{settings.SITE_URL}newsportal/',
                }
            )

            msg = EmailMultiAlternatives(
                subject='Статьи за неделю',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients,
            )

            msg.attach_alternative(html_content, 'text/html')

            msg.send()

@shared_task
def new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.posts_mtm.all()
    subscribers: list[str] = []
    for cat in categories:
        subscribers_user = cat.subscribers.all()
        for user in subscribers_user:
            subscribers.append(user.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview[:20]+"...",
            'link': f'{settings.SITE_URL}newsportal/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=post.heading,
        body=post.preview,
        from_email='uvedomleniynewsportal@ya.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()
