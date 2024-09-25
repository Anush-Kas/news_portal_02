import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.core.mail import EmailMultiAlternatives

from datetime import datetime, timedelta

from posts.models import Post, User, Category

logger = logging.getLogger(__name__)


def my_job():
    users = User.objects.all()
    for user in users:
        user_categories = Category.objects.filter(subscribers__user=user)
        date = datetime.now() - timedelta(weeks=1)
        posts = Post.objects.filter(category__in=user_categories).filter(created_at__gt=date)
        text = ''
        html_content = ''
        subject = f'Новые статьи в категориях'
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


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")