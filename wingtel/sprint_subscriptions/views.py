from rest_framework import viewsets

from wingtel.att_subscriptions.models import Subscription
from wingtel.sprint_subscriptions.serializers import SprintSubscriptionSerializer


class SprintSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """
    queryset = Subscription.objects.filter(type_of_subscription='sprint')
    serializer_class = SprintSubscriptionSerializer
