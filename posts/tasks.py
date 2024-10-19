import time
from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from .models import Category, Post


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def send_to_subscribers(post_id):
    instance = Post.objects.get(pk=post_id)
    emails = User.objects.filter(
        subscriptions__category__in=instance.category.all()
    ).values_list('email', flat=True)
    subject = f'Новая статья в категории {instance.category}'

    text = ' '.join(instance.text.split()[:25])
    text_content = (
        f'{instance.title}\n'
        f'{text}...\n'
        f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Товар: {instance.title}<br>'
        f'Цена: {text}...<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на статью</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_posts():
    users = User.objects.all()
    for user in users:
        user_categories = Category.objects.filter(subscribers__user=user)
        date = datetime.now() - timedelta(weeks=1)
        posts = Post.objects.filter(category__in=user_categories).filter(created_at__gt=date)
        text = ''
        html_content = ''
        subject = 'Новые статьи в категориях'
        for post in posts:
            text += (
                f'{post.title}\n'
                f'{post.text[:200]}...\n'
                f'Ссылка на статью: http://127.0.0.1:8000{post.get_absolute_url()}\n'
            )
            html_content += (
                f'{post.title}<br>'
                f'{post.text[:200]}...<br><br>'
                f'<a href="http://127.0.0.1{post.get_absolute_url()}">'
                f'Ссылка на статью</a><br>'
            )
        msg = EmailMultiAlternatives(subject, text, None, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
