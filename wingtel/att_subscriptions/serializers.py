from rest_framework import serializers
from wingtel.att_subscriptions.models import ATTSubscription


class ATTSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ATTSubscription
        fields = "__all__"
