from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_gis.filters import InBBoxFilter


class ParkingException(exceptions.APIException):
    status_code = 403
    default_detail = _('Unknown error.')
    default_code = 'unknown_error'


class WGS84InBBoxFilter(InBBoxFilter):
    """Works like a normal InBBoxFilter but converts WGS84 to ETRS89"""
    def get_filter_bbox(self, request):
        bbox = super().get_filter_bbox(request)
        if bbox is None:
            return bbox

        bbox.srid = 4326
        bbox.transform(3879)
        return bbox


class VersionedReferenceSerializer(serializers.Serializer):
    id = serializers.CharField(min_length=1, required=True)
    version = serializers.IntegerField(min_value=1, required=True)
    className = serializers.CharField(required=False)