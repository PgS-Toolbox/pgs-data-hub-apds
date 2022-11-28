from rest_framework import viewsets, permissions

from parkings.api.rights.serializers import PermitAssignedRightSerializer, RightSpecificationsSerializer
from parkings.models import Permit, PaymentZone
from parkings.api.enforcement.permissions import IsEnforcer
from parkings.api.rights.filters import AssignedRightsFilter, RightsSpecificationsFilter


class AssignedRightsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsEnforcer]
    queryset = Permit.objects.all()
    serializer_class = PermitAssignedRightSerializer
    filterset_class = AssignedRightsFilter


class RightsSpecificationsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = PaymentZone.objects.all()
    serializer_class = RightSpecificationsSerializer
    filterset_class = RightsSpecificationsFilter