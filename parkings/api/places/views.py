from rest_framework import viewsets, permissions

from parkings.api.places.serializers import PlacesSerializer
from parkings.models import ParkingArea
from parkings.api.places.filters import PlacesFilter


class PlacesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = ParkingArea.objects.all()
    serializer_class = PlacesSerializer
    lookup_field = "origin_id"
    filterset_class = PlacesFilter
