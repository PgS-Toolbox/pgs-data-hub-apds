from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from parkings.api.sessions.serializers import SessionsSerializer, SessionsCreateUpdateSerializer
from parkings.models import Parking
from parkings.api.monitoring.permissions import IsMonitor
from parkings.api.operator.permissions import IsOperator
from parkings.api.sessions.filters import SessionsFilter


class SessionsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsMonitor | IsOperator]
    queryset = Parking.objects.all()
    serializer_class = SessionsSerializer
    lookup_field = "id"
    filterset_class = SessionsFilter

    def get_queryset(self):
        if hasattr(self.request.user, 'operator'):
            return super().get_queryset().filter(operator=self.request.user.operator)
        else:
            return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            return SessionsCreateUpdateSerializer
        elif self.action == "update":
            return SessionsCreateUpdateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        obj = self.perform_create(create_serializer)
        serializer = SessionsSerializer(obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'operator'):
            return Response("Only operator can create new sessions", status=status.HTTP_403_FORBIDDEN)
        
        return Parking.objects.create(operator=self.request.user.operator, **serializer.validated_data)