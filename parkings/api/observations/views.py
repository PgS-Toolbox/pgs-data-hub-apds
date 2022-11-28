from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from parkings.api.observations.serializers import ObservationsSerializer, ObservationsCreateUpdateSerializer
from parkings.models import ParkingCheck
from parkings.api.enforcement.permissions import IsEnforcer
from parkings.api.observations.filters import ObservationFilter
from parkings.api.enforcement.check_parking import ParkingCheck
from parkings.api.enforcement.check_parking import parking_check_result


class ObservationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsEnforcer]
    queryset = ParkingCheck.objects.all()
    serializer_class = ObservationsSerializer
    filterset_class = ObservationFilter
    
    def get_serializer_class(self):
        if self.action == "create":
            return ObservationsCreateUpdateSerializer
        elif self.action == "update":
            return ObservationsCreateUpdateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        obj = self.perform_create(create_serializer)
        serializer = ObservationsSerializer(obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        _, obj = parking_check_result(serializer.validated_data, self.request)
        return obj
