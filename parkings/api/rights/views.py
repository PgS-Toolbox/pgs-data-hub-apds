from rest_framework import viewsets, permissions

from parkings.api.rights.serializers import PermitAssignedRightSerializer, RightSpecificationsSerializer
from parkings.models import Permit, PaymentZone


class AssignedRightsViewSet(viewsets.ReadOnlyModelViewSet):
    #permission_classes = []
    queryset = Permit.objects.all()
    serializer_class = PermitAssignedRightSerializer


class RightsSpecificationsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = PaymentZone.objects.all()
    serializer_class = RightSpecificationsSerializer