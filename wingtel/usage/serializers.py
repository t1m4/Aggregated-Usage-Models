from rest_framework import serializers

from wingtel.usage.models import BothUsageRecord


class ExceededPriceSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()
    price_exceeded = serializers.IntegerField()
    type_of_usage = serializers.ChoiceField(choices=BothUsageRecord.USAGE_TYPES)
    type_of_subscription = serializers.ChoiceField(choices=BothUsageRecord.SUBSCRIPTION_TYPE)