from rest_framework import viewsets

from parkings.api.observations.serializers import ObservationsSerializer, ObservationsCreateUpdateSerializer
from parkings.models import ParkingCheck
from parkings.api.enforcement.permissions import IsEnforcer


class ObservationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsEnforcer]
    queryset = ParkingCheck.objects.all()
    serializer_class = ObservationsSerializer
    
    def get_serializer_class(self):
        if self.action == "create":
            return ObservationsCreateUpdateSerializer
        elif self.action == "update":
            return ObservationsCreateUpdateSerializer
        return super().get_serializer_class()