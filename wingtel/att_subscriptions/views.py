from rest_framework import mixins, viewsets
from rest_framework.response import Response

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.att_subscriptions.serializers import ATTSubscriptionSerializer


class ATTSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """
    queryset = ATTSubscription.objects.all()
    serializer_class = ATTSubscriptionSerializer
