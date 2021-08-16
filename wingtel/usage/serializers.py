from rest_framework import serializers

from wingtel.usage.models import BothUsageRecord


class PriceLimitSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()
    price_exceeded = serializers.IntegerField()
    type_of_usage = serializers.ChoiceField(choices=BothUsageRecord.USAGE_TYPES)
    type_of_subscription = serializers.ChoiceField(choices=BothUsageRecord.SUBSCRIPTION_TYPE)


class PriceLimitDeserializer(serializers.Serializer):
    price_limit = serializers.IntegerField(min_value=1)


class SubscriptionUsageMetricsSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()
    total_price = serializers.IntegerField()
    total_used = serializers.IntegerField()
