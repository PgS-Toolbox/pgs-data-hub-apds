from rest_framework import serializers

from parkings.models import Parking


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
                "className": "registration_number",
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
                        "className": "registration_number",
                        "id": obj.normalize_reg_num
                        },
                    "issuer": [{
                        "language": "en",
                        "string": ""
                    }]
                }],
                "rightSpecification": {
                    "id": obj.id,
                    "version": 1
                },
                "expiry": obj.time_end,
                "issuanceTime": obj.created_at,
            },
            "validationType": [
                "licensePlate"
            ]
        }]