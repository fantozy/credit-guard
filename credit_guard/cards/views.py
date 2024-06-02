from django.http import HttpRequest

from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from .models import Card
from .filters import CardFilter
from .serializers import CardCreateSerializer, CardSerializer


class CardViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CardFilter
    serializer_class = CardCreateSerializer
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user).order_by("-created_at")

    def list(self, request: HttpRequest):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = CardSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request: HttpRequest):
        serializer = CardCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        card_serializer = CardSerializer(serializer.instance)

        return Response(card_serializer.data, status=status.HTTP_201_CREATED)
