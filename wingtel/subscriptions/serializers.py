from rest_framework import serializers

from wingtel.subscriptions.models import Subscription


class ATTSubscriptionSerializer(serializers.ModelSerializer):
    type_of_subscription = serializers.HiddenField(default=Subscription.SUBSCRIPTION_TYPE.att)

    class Meta:
        model = Subscription
        exclude = ["sprint_id"]


class SprintSubscriptionSerializer(serializers.ModelSerializer):
    type_of_subscription = serializers.HiddenField(default=Subscription.SUBSCRIPTION_TYPE.sprint)

    class Meta:
        model = Subscription
        exclude = ["network_type"]
