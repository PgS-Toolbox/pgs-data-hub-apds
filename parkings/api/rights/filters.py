import django_filters as filters

from parkings.models import Permit, PaymentZone


class AssignedRightsFilter(filters.FilterSet):
    credential_type = ,
    credential_class = ,
    credential_id = ,
    latitude = filters.NumberFilter(field_name="latitude", method="filter_location")
    longitude = filters.NumberFilter(field_name="longitude", method="filter_location")
    radius = filters.NumberFilter(field_name="radius", method="filter_location")
    modified_since
    start_before = 
    end_before = 
    start_after = 
    end_after = 

    class Meta:
        model = Permit
        fields =(

        )


class RightsSpecificationsFilter(filters.FilterSet):
    latitude = filters.NumberFilter(field_name="latitude", method="filter_location")
    longitude = filters.NumberFilter(field_name="longitude", method="filter_location")
    radius = filters.NumberFilter(field_name="radius", method="filter_location")
    modified_since
    credential_type

    class Meta:
        model = PaymentZone
        fields = (
            
        )