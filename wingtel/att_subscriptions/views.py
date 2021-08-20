from rest_framework import viewsets

from wingtel.att_subscriptions.models import Subscription
from wingtel.att_subscriptions.serializers import ATTSubscriptionSerializer


class ATTSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """
    queryset = Subscription.objects.filter(type_of_subscription='att')
    serializer_class = ATTSubscriptionSerializer
