import django_filters as filters

from parkings.models import Parking


class SessionsFilter(filters.FilterSet):
    right_spec = filters.CharFilter(field_name="right_spec", method="filter_right_spec")
    credential_type = filters.CharFilter(field_name="credential_type", method="filter_credential_type")
    credential_class = filters.CharFilter(field_name="credential_class", method="filter_credential_class")
    credential_id = filters.CharFilter(field_name="credential_id", method="filter_credential_id")
    latitude = filters.NumberFilter(field_name="latitude", method="filter_location")
    longitude = filters.NumberFilter(field_name="longitude", method="filter_location")
    radius = filters.NumberFilter(field_name="radius", method="filter_location")
    modified_since = filters.NumberFilter(field_name="modified_at", method="filter_modified_since")
    start_before = filters.NumberFilter(field_name="time_start", method="filter_start_before")
    end_before = filters.NumberFilter(field_name="time_end", method="filter_end_before")
    start_after = filters.NumberFilter(field_name="time_start", method="filter_start_after")
    end_after = filters.NumberFilter(field_name="time_end", method="filter_end_after")

    def filter_right_spec(self, queryset, name, value):
        return queryset.filter(domain__code=value)

    def filter_credential_type(self, queryset, name, value):
        if value == "licensePlate":
            return queryset
        else:
            return Parking.objects.none()

    def filter_credential_class(self, queryset, name, value):
        if value == "RegistrationNumber":
            return queryset
        else:
            return Parking.objects.none()

    def filter_credential_id(self, queryset, name, value):
        return queryset.filter(normalized_reg_num=value)

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

    def filter_start_before(self, queryset, name, value):
        return queryset.filter(time_start__lte=datetime.fromtimestamp(value))

    def filter_end_before(self, queryset, name, value):
        return queryset.filter(time_end__lte=datetime.fromtimestamp(value))

    def filter_start_after(self, queryset, name, value):
        return queryset.filter(time_start__gte=datetime.fromtimestamp(value))

    def filter_end_after(self, queryset, name, value):
        return queryset.filter(time_end__gte=datetime.fromtimestamp(value))