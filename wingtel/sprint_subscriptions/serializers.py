from rest_framework import serializers
from wingtel.sprint_subscriptions.models import SprintSubscription


class SprintSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SprintSubscription
        fields = '__all__'
