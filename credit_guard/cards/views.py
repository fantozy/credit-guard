from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .models import Card
from .serializers import CardCreateSerializer, CardSerializer


class CardViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user).order_by("-created_at")

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CardSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = CardCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(
            CardSerializer(serializer.instance).data, status=status.HTTP_201_CREATED
        )
