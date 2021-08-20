from rest_framework import serializers

from wingtel.att_subscriptions.models import Subscription


class SprintSubscriptionSerializer(serializers.ModelSerializer):
    type_of_subscription = serializers.HiddenField(default=Subscription.SUBSCRIPTION_TYPE.sprint)
    class Meta:
        model = Subscription
        exclude = ['network_type']