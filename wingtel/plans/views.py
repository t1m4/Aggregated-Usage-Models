from rest_framework import viewsets

from wingtel.plans.models import Plan
from wingtel.plans.serializers import PlanSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer