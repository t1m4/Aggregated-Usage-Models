from django.db.models import CharField, Sum, Value

from wingtel.usage.models import DataUsageRecord, UsageRecord, VoiceUsageRecord


def get_usage_records_with_exceeded_price(price_limit: int):
    """
    Return usage records fields(type_of_usage, subscription_id, price_exceeded)
    group by type_of_usage and subscription_id
    """
    return (
        UsageRecord.objects.filter()
        .values("type_of_usage", "subscription_id")
        .annotate(total_price=Sum("price"), price_exceeded=Sum("price") - price_limit)
        .filter(total_price__gt=price_limit)
        .values(
            "type_of_usage",
            "subscription_id",
            "price_exceeded",
        )
    )


def get_usage_records_group_by_subscription_id(subscription_id):
    """Return usage records(subscription_id, price, used) group by subscription_id"""
    return (
        UsageRecord.objects.filter(
            subscription_id=subscription_id,
        )
        .values("subscription_id")
        .annotate(
            total_price=Sum("price"),
            total_used=Sum("used"),
        )
    )


def get_data_usage_records_group_by():
    """Return usage records group by subscription_id and usage_date__date"""
    return (
        DataUsageRecord.objects.all()
        .values("usage_date__date", "subscription_id")
        .annotate(
            type_of_usage=Value(UsageRecord.USAGE_TYPES.data, output_field=CharField(max_length=5)),
            total_price=Sum("price"),
            total_used=Sum("kilobytes_used"),
        )
        .values("type_of_usage", "subscription_id", "total_price", "usage_date__date", "total_used")
        .iterator()
    )


def get_voice_usage_records_group_by():
    """Return usage records group by subscription_id and usage_date__date"""
    return (
        VoiceUsageRecord.objects.all()
        .values("usage_date__date", "subscription_id")
        .annotate(
            type_of_usage=Value(UsageRecord.USAGE_TYPES.voice, output_field=CharField(max_length=5)),
            total_price=Sum("price"),
            total_used=Sum("seconds_used"),
        )
        .values("type_of_usage", "subscription_id", "total_price", "usage_date__date", "total_used")
        .iterator()
    )
