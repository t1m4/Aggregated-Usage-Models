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

    type_of_subscription = models.CharField(max_length=100, choices=SUBSCRIPTION_TYPE)
    subscription_id = models.IntegerField()
    type_of_usage = models.CharField(max_length=100, choices=USAGE_TYPES)
    price = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    usage_date = models.DateField(null=False)
    used = models.IntegerField(null=False)

    @classmethod
    def check_sub_type(cls, type):
        """
        Check subscription_type
        """
        sub_type_exist = False
        for subscription_type in cls.SUBSCRIPTION_TYPE:
            if type == subscription_type[0]:
                sub_type_exist = True
                break
        return sub_type_exist