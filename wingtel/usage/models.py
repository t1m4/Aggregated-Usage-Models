from django.db import models
from model_utils import Choices

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.sprint_subscriptions.models import SprintSubscription


class DataUsageRecord(models.Model):
    """Raw data usage record for a subscription"""
    att_subscription_id = models.ForeignKey(ATTSubscription, null=True, on_delete=models.PROTECT)
    sprint_subscription_id = models.ForeignKey(SprintSubscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(null=False)
    kilobytes_used = models.IntegerField(null=False)


class VoiceUsageRecord(models.Model):
    """Raw voice usage record for a subscription"""
    att_subscription_id = models.ForeignKey(ATTSubscription, null=True, on_delete=models.PROTECT)
    sprint_subscription_id = models.ForeignKey(SprintSubscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(null=False)
    seconds_used = models.IntegerField(null=False)


class BothUsageRecord(models.Model):
    USAGE_TYPES = Choices(
        ('data', 'DataUsage'),
        ('voice', 'VoiceUsage'),
    )
    SUBSCRIPTION_TYPE = Choices(
        ('att', 'Att'),
        ('sprint', 'Sprint'),

    )
    subscription_id = models.IntegerField()
    type_of_subscription = models.CharField(max_length=100, choices=SUBSCRIPTION_TYPE)
    type_of_usage = models.CharField(max_length=100, choices=USAGE_TYPES)
    price = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    usage_date = models.DateField(null=False)
    used = models.IntegerField(null=False)
