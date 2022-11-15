from rest_framework import serializers

from parkings.models import Parking
from parkings.api.operator.parking import OperatorAPIParkingSerializer
from parkings.api.constants import CREDENTIAL_TYPES
from parkings.api.common import VersionedReferenceSerializer
from parkings.api.rights.serializers import AssignedRightSerializer, CredentialAssignedSerializer


class SessionsSerializer(serializers.ModelSerializer):
    actualStart = serializers.SerializerMethodField()
    actualEnd = serializers.SerializerMethodField()
    initiator = serializers.SerializerMethodField()
    identifiedCredentials = serializers.SerializerMethodField()
    segments = serializers.SerializerMethodField()

    class Meta:
        model = Parking
        fields = (
            "actualStart",
            "actualEnd",
            "initiator",
            "identifiedCredentials",
            "segments"
        )

    def get_actualStart(self, obj):
        return obj.time_start

    def get_actualEnd(self, obj):
        return obj.time_end

    def get_initiator(self, obj):
        return {
            "id": obj.operator.id,
            "version": 1,
            "className": "Operator"
        }

    def get_identifiedCredentials(self, obj):
        return [{
            "identifier": {
                "className": "RegistrationNumber",
                "id": obj.normalized_reg_num
            },
            "issuer": [{
                "language": "en",
                "string": ""
            }],
            "type": "licensePlate"
        }]

    def get_segments(self, obj):
        return [{
            "id": obj.id,
            "version": 1,
            "actualStart": obj.time_start,
            "actualEnd": obj.time_end,
            "assignedRight": {
                "id": obj.id,
                "version": 1,
                "rightHolder": [{
                    "identifier": {
                        "className": "RegistrationNumber",
                        "id": obj.normalized_reg_num
                        },
                    "issuer": [{
                        "language": "en",
                        "string": "",
                    }]
                }],
                "rightSpecification": {
                    "id": obj.zone.number,
                    "version": 1,
                    "className": "ParkingZone"
                },
                "expiry": obj.time_end,
                "issuanceTime": obj.created_at,
            },
            "validationType": [
                "licensePlate"
            ]
        }]


class SegmentsSerializer(serializers.Serializer):
    id = serializers.CharField(min_length=1, required=True)
    version = serializers.IntegerField(min_value=1, required=True)
    actualStart = serializers.DateTimeField(required=True)
    actualEnd = serializers.DateTimeField(required=False)
    assignedRight = AssignedRightSerializer()
    validationType = serializers.MultipleChoiceField(choices=CREDENTIAL_TYPES)


class SessionsCreateUpdateSerializer(serializers.ModelSerializer):
    actualStart = serializers.DateTimeField(required=True)
    actualEnd = serializers.DateTimeField(required=False)
    initiator = VersionedReferenceSerializer()
    identifiedCredentials = serializers.ListField(
        child=CredentialAssignedSerializer(),
        allow_empty=False
    )
    segments = serializers.ListField(child=SegmentsSerializer(), allow_empty=False)

    class Meta:
        model = Parking
        fields = (
            "actualStart",
            "actualEnd",
            "initiator",
            "identifiedCredentials",
            "segments"
        )

    def create(self, validated_data):
        return OperatorAPIParkingSerializer(data=validated_data)

    def validate(self, data):
        registration_number = ""
        for credentials in data["identifiedCredentials"]:
            if credentials["type"] == "licensePlate":
                registration_number = credentials["identifier"].get("id")
        if registration_number == "":
            raise serializers.ValidationError("There is no 'licensePlate' in `identifiedCredentials`")

        parking_zone = None
        for segment in data["segments"]:
            if segment["assignedRight"]["rightSpecification"]["className"] == "ParkingZone":
                if not parking_zone:
                    parking_zone = segment["assignedRight"]["rightSpecification"]["id"]
                elif parking_zone != segment["assignedRight"]["rightSpecification"]["id"]:
                    raise serializers.ValidationError("Different parking zones in one session")
        if parking_zone is None:
            raise serializers.ValidationError("No information about parking zone")

        if data["initiator"]["className"] != "Operator":
            raise serializers.ValidationError("Initiator className should be: Operator")

        parking_data = {
            #"location": None,
            #"terminal_number": None,
            "registration_number": registration_number,
            "time_start": data["actualStart"],
            "time_end": data.get("actualEnd"),
            "zone": parking_zone,
            "operator": data["initiator"]["id"]
        }
        OperatorAPIParkingSerializer.validate(parking_data)
        return parking_data