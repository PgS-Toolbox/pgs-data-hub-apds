from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from parkings.api.sessions.serializers import SessionsSerializer, SessionsCreateUpdateSerializer
from parkings.models import Parking
from parkings.api.operator.parking import OperatorAPIParkingPermission
from parkings.api.sessions.filter import SessionsFilter


class SessionsViewSet(viewsets.ModelViewSet):
    permission_classes = [OperatorAPIParkingPermission]
    queryset = Parking.objects.all()
    serializer_class = SessionsSerializer
    lookup_field = "id"
    filterset_class = SessionsFilter

    def get_serializer_class(self):
        if self.action == "create":
            return SessionsCreateUpdateSerializer
        elif self.action == "update":
            return SessionsCreateUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        if serializer.data["operator"] == self.request.user.operator.id:
            serializer.save(operator=self.request.user.operator)
        else:
            return Response("Authentication token does not match operator id", status=status.HTTP_403_FORBIDDEN)
