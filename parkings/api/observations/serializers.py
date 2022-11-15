from rest_framework import serializers

from parkings.models import ParkingCheck


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
        fields(
            "id",
            "version"
        )

    def get_id(self, obj):
        return obj.pk

    def get_version(self, obj):
        return 1

    def get_method(self, obj):
        return "visual"

    def get_observer(self, obj):
        return obj.performer.name

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
            "observerLocation": obj.location
        }

    def get_observerOrganisation(self, obj):
        return {
            "id": obj.performer.enforced_domain.code,
            "version": 1,
            "className": "EnforcementDomain"
        }