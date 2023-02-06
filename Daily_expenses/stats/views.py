# views.py
from rest_framework import viewsets
from rest_framework import permissions
from API.serializers import ExpensesSerializer
from django.db.models import Q
from API.models import Expenses
from categories.models import Categories
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from django.db import connection
from accounts.models import CustomUser
from datetime import date


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


class StatsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Expenses.objects.all().order_by('name')
    serializer_class = ExpensesSerializer

    def get_queryset(self):
        return self.queryset.filter(
            Q(user=self.request.user) |
            Q(user__isnull=True)
        )

    def send(self, subject, message, recipients):
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

    def list(self, request, *args, **kwargs):
        expenses = Expenses.objects.filter(
            Q(user=self.request.user))

        today = datetime.today()
        week = today - timedelta(days=7)
        month = today - timedelta(days=30)
        yesterday = today - timedelta(days=1)

        last_30_days_total = expenses.filter(date__gte=month).aggregate(
            Sum('price', field="price"))
        last_1_day_total = expenses.filter(date__gte=yesterday).aggregate(
            Sum('price', field="price"))
        last_7_days_total = expenses.filter(date__gte=week).aggregate(
            Sum('price', field="price"))

        results_price = sorted(Expenses.objects.filter(
            Q(user=self.request.user), date__gte=(
                datetime.now()-timedelta(days=30))).values('category_id')
            .annotate(total_price=Sum('price')),
            key=lambda x: x['total_price'])[-1]
        results_count = sorted(Expenses.objects.filter(
            Q(user=self.request.user),
            date__gte=(datetime.now()-timedelta(days=30)))
            .values('category_id')
            .annotate(count=Count('category')), key=lambda x: x['count'])[-1]
        most_popular_category = Categories.objects.get(
            id=results_price['category_id'])
        most_pricey_category = Categories.objects.get(
            id=results_count['category_id'])

        statistics = {
            'email': self.request.user.email,
            'balance_sheet': {
                'last_1_day': last_1_day_total,
                'last_7_days': last_7_days_total,
                'last_30_days': last_30_days_total,
            },
            'most_popular_category': most_popular_category.name,
            'invested_the_most_in': most_pricey_category.name
        }

        self.send(
            "Statistici",
            statistics,
            [self.request.user.email, "mailteste0404@gmail.com"]
        )

        return Response(
            {
                'user_statistics': statistics,
                'status': status.HTTP_200_OK
            })

    # def send(self, subject, message, recipients):
    #     mail_body_html = render_to_string(
    #         '/Users/hartansilviu/WORK/bench-silviu-daily-expenses-backend/Daily_expenses/stats/templates/email.html',
    #         {'data': message}
    #     )

    #     mail = EmailMessage(
    #         subject=subject,
    #         body=mail_body_html,
    #         from_email=settings.EMAIL_HOST_USER,
    #         to=recipients
    #     )

    #     mail.content_subtype = "html"
    #     return mail.send()
