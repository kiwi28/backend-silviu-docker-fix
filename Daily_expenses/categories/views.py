# views.py
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CategoriesSerializer
from django.db.models import Q
from .models import Categories


class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Categories.objects.all().order_by('name')  # de implentat metoda
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        return self.queryset.filter(
            Q(user=self.request.user) |
            Q(user__isnull=True)
        )
