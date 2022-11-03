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
            "occupancyLevel"
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
        return None

    def get_occupancyLevel(self, obj):
        data = {
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
        return data