from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

import django_filters as filters

from parkings.models import ParkingArea


class PlacesFilter(filters.FilterSet):
    latitude = filters.NumberFilter(field_name="latitude", method="filter_location")
    longitude = filters.NumberFilter(field_name="longitude", method="filter_location")
    radius = filters.NumberFilter(field_name="radius", method="filter_location")
    
    class Meta:
        model = ParkingArea
        fields = (
            "latitude",
            "longitude",
            "radius"
        )
        
    def filter_location(self, queryset, name, value):
        params = self.request.query_params
        if params["latitude"] and params["longitude"] and params['radius']:
            center = Point(float(params["longitude"]), float(params["latitude"]))
            return (
                queryset.filter(
                    geom__distance_lte=(center, D(m=float(params["radius"])))
                )
            )
        return queryset
