from django.core.serializers import serialize

from rest_framework import serializers
from rest_framework_gis.serializers import GeometrySerializerMethodField

from parkings.models import ParkingCheck
from parkings.api.constants import CREDENTIAL_TYPES
from parkings.api.common import VersionedReferenceSerializer
from parkings.api.enforcement.check_parking import CheckParkingSerializer


class ObservationsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()
    method = serializers.SerializerMethodField()
    observer = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    observedCredentialId = serializers.SerializerMethodField()
    observationStartTime = serializers.SerializerMethodField()
    creationDateTime = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    observerOrganisation = serializers.SerializerMethodField()

    class Meta:
        model = ParkingCheck
        fields = (
            "id",
            "version",
            "method",
            "observer",
            "type",
            "observedCredentialId",
            "observationStartTime",
            "creationDateTime",
            "location",
            "observerOrganisation"
        )

    def get_id(self, obj):
        return obj.pk

    def get_version(self, obj):
        return 1

    def get_method(self, obj):
        return "visual"

    def get_observer(self, obj):
        if obj.performer.get_full_name():
            return obj.performer.get_full_name()
        else:
            return obj.performer.get_username()

    def get_type(self, obj):
        return "licensePlate"

    def get_observedCredentialId(self, obj):
        return obj.registration_number

    def get_observationStartTime(self, obj):
        return obj.time

    def get_creationDateTime(self, obj):
        return obj.created_at

    def get_location(self, obj):
        return {
            "observerLocation": serialize('geojson', (obj,), geometry_field='location', fields=('location',))
        }

    def get_observerOrganisation(self, obj):
        return {
            "id": obj.performer.enforcer.enforced_domain.code,
            "version": 1,
            "className": "EnforcementDomain"
        }


class GeoJsonGeometryPointSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=("Point",))
    coordinates = serializers.ListField(
        child=serializers.FloatField(min_value=-180, max_value=180),
        min_length=2,
        max_length=2
    )


class GeoJsonPointSerializer(serializers.Serializer):
    geometry = GeoJsonGeometryPointSerializer()


class LocationSerializerAPDS(serializers.Serializer):
    observerLocation = GeoJsonPointSerializer()


class ObservationsCreateUpdateSerializer(serializers.ModelSerializer):
    method = serializers.ChoiceField(choices=("anpr", "chalk", "rfTransponder", "scanner", "visual"))
    observer = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=CREDENTIAL_TYPES, required=True)
    observedCredentialId = serializers.CharField(max_length=20, required=True)
    observationStartTime = serializers.DateTimeField(required=True)
    location = LocationSerializerAPDS()
    observerOrganisation = VersionedReferenceSerializer()

    class Meta:
        model = ParkingCheck
        fields = (
            "method",
            "observer",
            "type",
            "observedCredentialId",
            "observationStartTime",
            "location",
            "observerOrganisation"
        )

    def validate(self, attrs):
        if attrs["type"] != "licensePlate":
            raise serializers.ValidationError("Type is different than `licensePlate`")

        if "observerLocation" not in attrs["location"].keys():
            raise serializers.ValidationError("No observerLocation")

        check_parking_data = {
            "registration_number": attrs["observedCredentialId"],
            "location": {
                "latitude": attrs["location"]["observerLocation"]["geometry"]["coordinates"][0],
                "longitude": attrs["location"]["observerLocation"]["geometry"]["coordinates"][1]
            },
            "time": attrs["observationStartTime"]
        }

        check_parking_serializer = CheckParkingSerializer(data=check_parking_data)
        check_parking_serializer.is_valid(raise_exception=True)
        
        return check_parking_serializer.validated_data