from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def post_created(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    if action != "post_add":
        return
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
