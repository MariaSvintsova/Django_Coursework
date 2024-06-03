
import pytz
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.conf import settings
from main.models import NewsLetter

class Message:
    def start():
        """ Функция старта периодических задач """
        scheduler = BackgroundScheduler()
        scheduler.add_job(функция_отправки_письма, 'interval', seconds=10)
        scheduler.start()

    # Главная функция по отправке рассылки
    def send_mailing():
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        mailings = NewsLetter.objects.filter(create_date__lte=current_datetime).filter(
            status__in=[NewsLetter.CREATED, NewsLetter.LAUNCHED])

        for mailing in mailings:
            last_attempt = mailing.attempt_set.order_by('-date').first()
            if last_attempt:
                last_send_time = last_attempt.date
                if mailing.frequency == NewsLetter.DAILY and (current_datetime - last_send_time).days >= 1:
                    next_send_time = last_send_time + timedelta(days=1)
                elif mailing.frequency == NewsLetter.WEEKLY and (current_datetime - last_send_time).days >= 7:
                    next_send_time = last_send_time + timedelta(weeks=1)
                elif mailing.frequency == NewsLetter.MONTHLY and (current_datetime - last_send_time).days >= 30:
                    next_send_time = last_send_time + timedelta(days=30)
                else:
                    continue
            else:
                next_send_time = current_datetime

            if next_send_time <= current_datetime:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.client.all()],
                )
                # Log attempt
                Attempt.objects.create(newsletter=mailing, date=current_datetime)