from django_cron import CronJobBase, Schedule
from django.db import connection
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# in acelasi job - user.all() + mail + refresh view


class TemplateViewRefreshCronJob(CronJobBase):
    RUN_AT_TIMES = ['11:30', '14:00', '23:15']
    RUN_EVERY_MINS = 5  # every 5 minutes
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'API.TemplateViewRefreshCronJob'    # a unique code

    def do(self):
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW stats_expenses")


class MailCronJob(CronJobBase):
    RUN_AT_TIMES = ['11:30', '14:00', '23:15']
    RUN_EVERY_MINS = 5  # every 5 minutes
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'API.MailCronJob'    # a unique code

    def do(self, subject, message, recipients):
        mail_body_html = render_to_string(
            '/Users/hartansilviu/WORK/bench-silviu-daily-expenses-backend/Daily_expenses/stats/templates/email.html',
            {'data': message}
        )

        mail = EmailMessage(
            subject=subject,
            body=mail_body_html,
            from_email=settings.EMAIL_HOST_USER,
            to=recipients
        )

        mail.content_subtype = "html"
        return mail.send()
