from django.db import connection


def do():
    with connection.cursor() as cursor:
        cursor.execute("REFRESH MATERIALIZED VIEW stats_expenses")


do()
