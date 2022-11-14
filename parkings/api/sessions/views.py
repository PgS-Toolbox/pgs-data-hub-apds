from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from parkings.api.sessions.serializers import SessionsSerializer
from parkings.models import Parking
from parkings.api.operator.parking import OperatorAPIParkingPermission


class SessionsViewSet(viewsets.ModelViewSet):
    permission_classes = [OperatorAPIParkingPermission]
    queryset = Parking.objects.all()
    serializer_class = SessionsSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        if serializer.data["operator"] == self.request.user.operator.id:
            serializer.save(operator=self.request.user.operator)
        else:
            return Response("Authentication token does not match operator id", status=status.HTTP_403_FORBIDDEN)
