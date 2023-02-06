# views.py
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ExpensesSerializer
from .models import Expenses
from rest_framework import status
from rest_framework.response import Response
from .models import Categories
from django.db.models import Q
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend


class ExpensesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Expenses.objects.all().order_by('name')
    serializer_class = ExpensesSerializer
    filter_backends = [DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        input_category = request.data['category']
        category_is_valid = (len(Categories.objects.filter(
            (
                Q(user=self.request.user) |
                Q(user__isnull=True)) &
            Q(id=input_category))) == 1
        )
        if category_is_valid:
            request.data['user'] = self.request.user.id
            if 'date' in request.data:
                request.data['date'] = datetime.fromtimestamp(
                    request.data['date']).date()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.initial_data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(
            "Current Logged User does not have access to the specified category", # noqa
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, *args, **kwargs):
        expenses = self.get_queryset()
        serializer = ExpensesSerializer(expenses, many=True)
        return Response({'expenses': serializer.data,
                         'status': status.HTTP_200_OK})

    def get_queryset(self):
        from_value = self.request.query_params.get("from", None)
        until_value = self.request.query_params.get("until", None)

        if from_value and until_value:
            from_date = datetime.fromtimestamp(int(from_value)).date()
            until_date = datetime.fromtimestamp(int(until_value)).date()
            qs = Expenses.objects.filter(
                Q(user=self.request.user),
                date__gte=from_date,
                date__lte=until_date
            )
        elif from_value and until_value is None:
            from_date = datetime.fromtimestamp(int(from_value)).date()
            qs = Expenses.objects.filter(
                Q(user=self.request.user),
                date__gte=from_date,
            )
        elif from_value is None and until_value:
            until_date = datetime.fromtimestamp(int(until_value)).date()
            qs = Expenses.objects.filter(
                Q(user=self.request.user),
                date__lte=until_date
            )
        else:
            qs = Expenses.objects.filter(Q(user=self.request.user))

        return qs
