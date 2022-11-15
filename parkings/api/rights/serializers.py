from rest_framework import serializers

from parkings.models import Permit
from parkings.api.common import (
    VersionedReferenceSerializer, 
    ReferenceSerializer, 
    MultilingualStringSerializer
)
from parkings.api.constants import CREDENTIAL_TYPES
from parkings.api.common_permit import PermitSerializer


class PermitAssignedRightSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()
    rightHolder = serializers.SerializerMethodField()
    rightSpecification = serializers.SerializerMethodField()
    expiry = serializers.SerializerMethodField()
    issuanceTime = serializers.SerializerMethodField()
    
    class Meta:
        model = Permit
        fields = (
            "id",
            "version",
            "rightHolder",
            "rightSpecification",
            "expiry",
            "issuanceTime"
        )

    def get_id(self, obj):
        return obj.pk

    def get_version(self, obj):
        return 1

    def get_rightHolder(self, obj):
        return [{
            "identifier": {
                "className": "RegistrationNumber",
                "id": subject["registration_number"]
            },
            "issuer": [{
                "language": "en",
                "string": "",
            }],
            "type": "licensePlate"
        } for subject in obj.subjects]

    def get_rightSpecification(self, obj):
        return {
            "id": obj.domain.code,
            "version": 1,
            "className": "Domain" 
        }

    def get_expiry(self, obj):
        return max([subject["end_time"] for subject in obj.subjects])

    def get_issuanceTime(self, obj):
        return min([subject["start_time"] for subject in obj.subjects])


class CredentialAssignedSerializer(serializers.Serializer):
    identifier = ReferenceSerializer()
    issuer = MultilingualStringSerializer()
    type = serializers.ChoiceField(choices=CREDENTIAL_TYPES)


class AssignedRightSerializer(serializers.Serializer):
    id = serializers.CharField(min_length=1, required=True)
    version = serializers.IntegerField(min_value=1, required=True)
    rightHolder = serializers.ListField(child=CredentialAssignedSerializer(), allow_empty=False)
    rightSpecification = VersionedReferenceSerializer()
    expiry = serializers.DateTimeField()
    issuanceTime = serializers.DateTimeField()
    assignedRightIssuer = ReferenceSerializer()


class PermitCreateAssignedRightSerializer(serializers.ModelSerializer):
    rightHolder = serializers.ListField(child=CredentialAssignedSerializer(), allow_empty=False)
    rightSpecification = VersionedReferenceSerializer()
    expiry = serializers.DateTimeField()
    issuanceTime = serializers.DateTimeField()
    
    class Meta:
        model = Permit
        fields = (
            "rightHolder",
            "rightSpecification",
            "expiry",
            "issuanceTime"
        )

    def create(self, validated_data):
        return PermitSerializer(**validated_data)

    def validate(self, data):
        # TODO
        return data
