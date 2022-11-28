from datetime import datetime

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

import django_filters as filters

from parkings.models import Permit, PaymentZone


class AssignedRightsFilter(filters.FilterSet):
    credential_type = filters.CharFilter(field_name="credential_type", method="filter_credential_type")
    credential_id = filters.CharFilter(field_name="credential_id", method="filter_credential_id")
    modified_since = filters.NumberFilter(field_name="modified_at", method="filter_modified_since")

    class Meta:
        model = Permit
        fields =(
            "credential_type",
            "credential_id",
            "modified_since",
        )

    def filter_credential_type(self, queryset, name, value):
        if value == "licensePlate":
            return queryset
        else:
            return Permit.objects.none()

    def filter_credential_id(self, queryset, name, value):
        return queryset.filter(subjects__contains={'registration_number': value})
    
    def filter_modified_since(self, queryset, name, value):
        return queryset.filter(modified_at__gte=datetime.fromtimestamp(value))


class RightsSpecificationsFilter(filters.FilterSet):
    latitude = filters.NumberFilter(field_name="latitude", method="filter_location")
    longitude = filters.NumberFilter(field_name="longitude", method="filter_location")
    radius = filters.NumberFilter(field_name="radius", method="filter_location")
    modified_since = filters.NumberFilter(field_name="modified_at", method="filter_modified_since")
    credential_type = filters.CharFilter(field_name="credential_type", method="filter_credential_type")

    class Meta:
        model = PaymentZone
        fields = (
            "latitude",
            "longitude",
            "radius",
            "modified_since",
            "credential_type"
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

    def filter_modified_since(self, queryset, name, value):
        return queryset.filter(modified_at__gte=datetime.fromtimestamp(value))

    def filter_credential_type(self, queryset, name, value):
        if value == "licensePlate":
            return queryset
        else:
            return PaymentZone.objects.none()