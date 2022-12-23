from rest_framework import viewsets

from wingtel.subscriptions.models import Subscription
from wingtel.subscriptions.serializers import (
    ATTSubscriptionSerializer,
    SprintSubscriptionSerializer,
)


class ATTSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """

    queryset = Subscription.objects.filter(type_of_subscription="att")
    serializer_class = ATTSubscriptionSerializer


class SprintSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """

    queryset = Subscription.objects.filter(type_of_subscription="sprint")
    serializer_class = SprintSubscriptionSerializer
