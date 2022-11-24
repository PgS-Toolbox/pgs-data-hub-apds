from django.core.serializers import serialize
from django.utils import timezone
from django.db.models import Q

from rest_framework import serializers

from parkings.models import ParkingArea


class PlacesSerializer(serializers.ModelSerializer):
    layer = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    hierarchyElementReference = serializers.SerializerMethodField()
    spaceBoundedZone = serializers.SerializerMethodField()
    
    class Meta:
        model = ParkingArea
        fields = (
            "layer",
            "type",
            "hierarchyElementReference",
            "spaceBoundedZone"
        )

    def get_layer(self, obj):
        return 1

    def get_type(self, obj):
        return "place"

    def get_hierarchyElementReference(self, obj):
        now = timezone.now()
        current_parking_count = obj.parkings.filter(
            Q(time_start__lte=now) & (Q(time_end__gte=now) | Q(time_end__isnull=True))
        ).count()
        
        return {
            "elementId": {
                "id": obj.origin_id,
                "version": 1,
                "className": "ParkingArea"
            },
            "demandTable": {
                "demandType": {
                    "count": current_parking_count,
                    "creationTime": now,
                    "occupancyCalculation": "derived",
                    "percentage": current_parking_count / obj.estimated_capacity
                }
            },
            "supply": {
                "supplyViewType": "vehicleView",
                "supplyQuantity": obj.estimated_capacity,
            }
        }

    def get_spaceBoundedZone(self, obj):
        return {
            "geoJSONPolygon": serialize('geojson', (obj,), geometry_field='geom', fields=('geom',))
        }