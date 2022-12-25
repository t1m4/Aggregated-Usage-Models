from django.db import models
from model_utils import Choices

from wingtel.subscriptions.models import Subscription


class DataUsageRecord(models.Model):
    """Raw data usage record for a subscription"""

    subscription_id = models.ForeignKey(Subscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(null=False)
    kilobytes_used = models.IntegerField(null=False)


class VoiceUsageRecord(models.Model):
    """Raw voice usage record for a subscription"""

    subscription_id = models.ForeignKey(Subscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(null=False)
    seconds_used = models.IntegerField(null=False)


class UsageRecord(models.Model):
    """Aggregate representation for usage record"""

    USAGE_TYPES = Choices(
        ("data", "DataUsage"),
        ("voice", "VoiceUsage"),
    )

    type_of_usage = models.CharField(max_length=100, choices=USAGE_TYPES, db_index=True)
    subscription = models.ForeignKey(Subscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    usage_date = models.DateField(null=False, db_index=True)
    used = models.IntegerField(null=False)


class UsageRecordView(models.Model):
    USAGE_TYPES = Choices(
        ("data", "DataUsage"),
        ("voice", "VoiceUsage"),
    )
    subscription_id = models.IntegerField()
    type_of_usage = models.CharField(max_length=100, choices=USAGE_TYPES)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    usage_date = models.DateField(null=False)
    used = models.IntegerField(null=False)

    class Meta:
        managed = False
        db_table = "usage_records_view"
