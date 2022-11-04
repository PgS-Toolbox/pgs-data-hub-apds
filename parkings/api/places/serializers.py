from django.core.serializers import serialize
from django.utils import timezone
from django.db.models import Q

from rest_framework import serializers

from parkings.models import ParkingArea


class PlacesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    layer = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    aliases = serializers.SerializerMethodField()
    parentId = serializers.SerializerMethodField()
    childIds = serializers.SerializerMethodField()
    operatorDefinedReference = serializers.SerializerMethodField()
    hierarchyElementRecord = serializers.SerializerMethodField()
    rightSpecifications = serializers.SerializerMethodField()
    hierarchyElementReference = serializers.SerializerMethodField()
    occupancyLevel = serializers.SerializerMethodField()
    spaceBoundedZone = serializers.SerializerMethodField()
    
    class Meta:
        model = ParkingArea
        fields = (
            "name",
            "description",
            "layer",
            "type",
            "aliases",
            "parentId",
            "childIds",
            "operatorDefinedReference",
            "hierarchyElementRecord",
            "rightSpecifications",
            "hierarchyElementReference",
            "occupancyLevel",
            "spaceBoundedZone"
        )

    def get_name(self, obj):
        return None

    def get_description(self, obj):
        return None

    def get_layer(self, obj):
        return 1

    def get_type(self, obj):
        return "place"

    def get_aliases(self, obj):
        return None

    def get_parentId(self, obj):
        return None

    def get_childIds(self, obj):
        return None

    def get_operatorDefinedReference(self, obj):
        return None

    def get_hierarchyElementRecord(self, obj):
        return None
    
    def get_rightSpecifications(self, obj):
        return None

    def get_hierarchyElementReference(self, obj):
        now = timezone.now()
        current_parking_count = obj.parkings.filter(
            Q(time_start__lte=now) & (Q(time_end__gte=now) | Q(time_end__isnull=True))
        ).count()
        
        return {
            "elementId": {
                "id": "string",
                "version": None,
                "className": None
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

    def get_occupancyLevel(self, obj):
        return {
            "occupancyIndicator": {
                "codeListEntryId": {
                    "className": None
                },
                "codeListId": {
                    "id": None,
                    "version": 1,
                    "className": None
                },
                "entryDefinedValue": None
            }
        }

    def get_spaceBoundedZone(self, obj):
        return {
            "geoJSONPolygon": serialize('geojson', (obj,), geometry_field='geom', fields=('geom',))
        }