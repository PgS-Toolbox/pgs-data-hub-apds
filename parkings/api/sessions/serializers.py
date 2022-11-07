from rest_framework import serializers

from parkings.models import Parking


class IdentifiedCredentialsSerializer(serializers.ModelSerializer):
    pass


class SegmentsSerializer(serializers.ModelSerializer):
    pass


class SessionsSerializer(serializers.ModelSerializer):
    actualStart = serializers.SerializerMethodField()
    actualEnd = serializers.SerializerMethodField()
    identifiedCredentials = IdentifiedCredentialsSerializer()
    segments = SegmentsSerializer()

    class Meta:
        model = Parking
        fields = (
            ,
        )
