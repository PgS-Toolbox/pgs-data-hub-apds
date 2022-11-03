from rest_framework import viewsets

from parkings.api.places.serializers import PlacesSerializer
from parkings.models import ParkingArea


class PlacesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParkingArea.objects.all()
    serializer_class = PlacesSerializer
    lookup_field = "origin_id"
