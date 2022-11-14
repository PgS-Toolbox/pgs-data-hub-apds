from rest_framework import serializers

from parkings.models import Parking
from parkings.api.operator.parking import OperatorAPIParkingSerializer


class SessionsSerializer(serializers.ModelSerializer):
    actualStart = serializers.SerializerMethodField(required=True)
    actualEnd = serializers.SerializerMethodField(required=False)
    initiator = serializers.SerializerMethodField(required=True)
    identifiedCredentials = serializers.SerializerMethodField(required=True)
    segments = SegmentsSerializer(required=True)

    class Meta:
        model = Parking
        fields = (
            "actualStart",
            "actualEnd"
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
                if identifier := credentials.get("identifier"):
                    registration_number = identifier.get("id")
                else:
                    raise serializers.ValidationError("No 'id' in identifiedCredentials identifier")
            else:
                raise serializers.ValidationError("No 'identifier' in identifiedCredentials")
        if registration_number == "":
            raise serializers.ValidationError("There is no 'licensePlate' in `identifiedCredentials`")

        parking_zone = None
        if type(data["segments"]) != list:
            raise serializers.ValidationError("Wrong type for 'segments', should be a list")
        for segment in data["segments"]:
            if type(segment) != dict:
                raise serializers.ValidationError("Wrong type for segment, should be a dict")
            if assign_right := segment.get("assignedRight"):
                if right_specification := assign_right.get("rightSpecification"):
                    if right_specification.get("className") and right_specification.get("className") == "ParkingZone":
                        if parking_zone is None:
                            parking_zone = right_specification.get("id")
                        elif parking_zone != right_specification.get("id"):
                            raise serializers.ValidationError("Different parking zones in one session")

        if parking_zone is None:
            raise serializers.ValidationError("No information about parking zone")

        parking_data = {
            #"location": None,
            #"terminal_number": None,
            "registration_number": registration_number,
            "time_start": data["actualStart"],
            "time_end": data.get("actualEnd"),
            "zone": parking_zone,  
        }
        OperatorAPIParkingSerializer.validate(parking_data)
        return parking_data


    def get_actualStart(self, obj):
        return obj.time_start

    def get_actualEnd(self, obj):
        return obj.time_end

    def get_initiator(self, obj):
        return {
            "id": obj.operator.id,
            "version": 1,
            "className": "operator"
        }

    def get_identifiedCredentials(self, obj):
        return [{
            "identifier": {
                "className": "RegistrationNumber",
                "id": obj.normalize_reg_num
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
                        "id": obj.normalize_reg_num
                        },
                    "issuer": [{
                        "language": "en",
                        "string": "",
                    }]
                }],
                "rightSpecification": {
                    "id": obj.zone,
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