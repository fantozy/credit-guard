# filters.py
from django_filters import rest_framework as filters
from .models import Card


class CardFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Card
        fields = ["title"]
