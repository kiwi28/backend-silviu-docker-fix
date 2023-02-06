from datetime import date
from django.core.management.base import BaseCommand
from django.db import connection
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import CustomUser
from API.models import StatsExpensesMaterializedView
from django.db.models import Q
from django.db.models import Sum
import pdb


class Command(BaseCommand):
    args = ''
    help = 'Send weekly statistics to users and refresh stats_expenses view.'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW stats_expenses")

        for user in CustomUser.objects.all():
            subject = "Statistici"
            todays_date = date.today()
            current_day = todays_date.day
            current_month = todays_date.month
            current_year = todays_date.year

            expenses = StatsExpensesMaterializedView.objects.filter(
                Q(user_id=user.id))

            last_30_days_total = expenses.filter(month=current_month, year=current_year).aggregate(
                Sum('total', field="total"))

            last_1_day_total = expenses.filter(day=current_day, month=current_month, year=current_year).aggregate(
                Sum('total', field="total"))

            last_7_days_total = expenses.filter(
                day__gte=current_day-7,
                day__lte=current_day,
                month=current_month,
                year=current_year
            ).aggregate(
                Sum('total', field="total"))

            pdb.set_trace()

            message = {
                'email': user.email,
                'balance_sheet': {
                    'last_1_day': last_1_day_total,
                    'last_7_days': last_7_days_total,
                    'last_30_days': last_30_days_total,
                }
            }

            pdb.set_trace()

            self.send_mail(
                subject,
                message,
                [user.email, ])

    def send_mail(self, subject, message, recipients):
        mail_body_html = render_to_string(
            '/Users/hartansilviu/WORK/bench-silviu-daily-expenses-backend/Daily_expenses/API/templates/email.html',
            {'data': message}
        )

        pdb.set_trace()

        mail = EmailMessage(
            subject=subject,
            body=mail_body_html,
            from_email=settings.EMAIL_HOST_USER,
            to=recipients
        )

        pdb.set_trace()

        mail.content_subtype = "html"
        return mail.send()
