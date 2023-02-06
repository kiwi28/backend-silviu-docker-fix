# models.py
from django.db import models
from categories.models import Categories
from accounts.models import CustomUser
from datetime import date


class StatsExpensesMaterializedView(models.Model):
    user_id = models.IntegerField(db_column='user_id')
    total = models.FloatField(db_column='total')
    day = models.IntegerField(db_column='day')
    month = models.IntegerField(db_column='month')
    year = models.IntegerField(db_column='year')

    class Meta:
        managed = False
        db_table = 'stats_expenses'


class Expenses(models.Model):
    name = models.CharField(max_length=60)
    amount = models.IntegerField(default=0)
    price = models.FloatField()
    currency = models.CharField(max_length=60)
    category = models.ForeignKey(Categories, null=True, blank=True,
                                 on_delete=models.CASCADE)
    additional_info = models.CharField(max_length=100, null=True)
    # date = models.DateField(default=datetime.today().date())
    # django.utils.timezone.now
    date = models.DateField(default=date.today)
    # date = models.DateField(auto_now_add=True)
    # date = UnixTimeStampField(default=date.today)
    # date = models.IntegerField()
    user = models.ForeignKey(CustomUser, default=None, blank=True, null=True,
                             on_delete=models.CASCADE)
