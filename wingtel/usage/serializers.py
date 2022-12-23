from rest_framework import serializers

from wingtel.usage.models import UsageRecord


class UsageRecordExceedingPriceSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()
    price_exceeded = serializers.IntegerField()
    type_of_usage = serializers.ChoiceField(choices=UsageRecord.USAGE_TYPES)


class PriceLimitDeserializer(serializers.Serializer):
    price_limit = serializers.IntegerField(min_value=1)


class UsageRecordTotalMetricsSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()
    total_price = serializers.IntegerField()
    total_used = serializers.IntegerField()
