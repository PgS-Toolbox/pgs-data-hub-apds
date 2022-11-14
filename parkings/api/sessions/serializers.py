from rest_framework import serializers

from parkings.models import Parking
from parkings.api.operator.parking import OperatorAPIParkingSerializer


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

    def create(self, validated_data):
        return OperatorAPIParkingSerializer(data=validated_data)

    def validate(self, data):
        registration_number = ""
        for credentials in data["identifiedCredentials"]:
            if credentials["type"] == "licensePlate":
                if credentials.get("identifier"):
                    registration_number = credentials["identifier"].get("id")
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
            if segment.get("assignedRight"):
                if segment["assignedRight"].get("rightSpecification"):
                    if segment["assignedRight"]["rightSpecification"].get("className") and segment["assignedRight"]["rightSpecification"].get("className") == "ParkingZone":
                        if parking_zone is None:
                            parking_zone = segment["assignedRight"]["rightSpecification"].get("id")
                        elif parking_zone != segment["assignedRight"]["rightSpecification"].get("id"):
                            raise serializers.ValidationError("Different parking zones in one session")

        if parking_zone is None:
            raise serializers.ValidationError("No information about parking zone")

        if type(data["initiator"]) != dict:
            raise serializers.ValidationError("Wrong type for 'initiator', should be a dict")
        else:
            operator = data["initiator"].get("id")

        parking_data = {
            #"location": None,
            #"terminal_number": None,
            "registration_number": registration_number,
            "time_start": data["actualStart"],
            "time_end": data.get("actualEnd"),
            "zone": parking_zone,
            "operator": operator
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