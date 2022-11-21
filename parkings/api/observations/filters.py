import django_filters as filters

from parkings.models import ParkingCheck


class ObservationFilter(filters.FilterSet):
    latitude = filters.NumberFilter(field_name="latitude", method="filter_location")
    longitude = filters.NumberFilter(field_name="longitude", method="filter_location")
    radius = filters.NumberFilter(field_name="radius", method="filter_location")
    start_before = filters.NumberFilter(field_name="time", method="filter_start_before")
    start_after = filters.NumberFilter(field_name="time", method="filter_start_after")

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

    def filter_start_before(self, queryset, name, value):
        return queryset.filter(time__lte=datetime.fromtimestamp(value)) 

    def filter_start_after(self, queryset, name, value):
        return queryset.filter(time__gte=datetime.fromtimestamp(value)) 