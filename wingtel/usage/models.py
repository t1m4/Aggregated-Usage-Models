from django.db import models
from model_utils import Choices

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.sprint_subscriptions.models import SprintSubscription
from wingtel.usage.utils import get_object_or_none


class DataUsageRecord(models.Model):
    """Raw data usage record for a subscription"""
    att_subscription_id = models.ForeignKey(ATTSubscription, null=True, on_delete=models.PROTECT)
    sprint_subscription_id = models.ForeignKey(SprintSubscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(null=False)
    kilobytes_used = models.IntegerField(null=False)

    def save(self, *args, **kwargs):
        super(DataUsageRecord, self).save(*args, **kwargs)

        record_type = 'data'
        # check exist entry with this params
        if self.att_subscription_id:
            record = get_object_or_none(BothUsageRecord, subscription_id=self.att_subscription_id.id,
                                        usage_date=self.usage_date.date(), type_of_usage=record_type,
                                        type_of_subscription='att')
        else:
            record = get_object_or_none(BothUsageRecord, subscription_id=self.sprint_subscription_id.id,
                                        usage_date=self.usage_date.date(), type_of_usage=record_type,
                                        type_of_subscription='sprint')
        if record:
            self.__update_aggregate_obj(record)
        else:
            BothUsageRecord.objects.create_aggregate_obj(self, record_type)

    def __update_aggregate_obj(self, old_obj):
        """
        Update price and used for new field
        """
        old_obj.price += self.price
        old_obj.used += self.kilobytes_used
        old_obj.save(update_fields=['price', 'used'])


class VoiceUsageRecord(models.Model):
    """Raw voice usage record for a subscription"""
    att_subscription_id = models.ForeignKey(ATTSubscription, null=True, on_delete=models.PROTECT)
    sprint_subscription_id = models.ForeignKey(SprintSubscription, null=True, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    usage_date = models.DateTimeField(null=False)
    seconds_used = models.IntegerField(null=False)

    def save(self, *args, **kwargs):
        super(VoiceUsageRecord, self).save(*args, **kwargs)

        record_type = 'voice'
        # check exist entry with this params
        if self.att_subscription_id:
            subscription_id = self.att_subscription_id.id
            type_of_subscription = 'att'
        else:
            subscription_id = self.sprint_subscription_id.id
            type_of_subscription = 'sprint'
        record = get_object_or_none(BothUsageRecord, subscription_id=subscription_id,
                                    usage_date=self.usage_date.date(), type_of_usage=record_type,
                                    type_of_subscription=type_of_subscription)

        if record:
            self.__update_aggregate_obj(record)
        else:
            BothUsageRecord.objects.create_aggregate_obj(self, record_type)

    def __update_aggregate_obj(self, old_obj):
        """
        Update price and used for new field
        """
        old_obj.price += self.price
        old_obj.used += self.seconds_used
        old_obj.save(update_fields=['price', 'used'])


class BothUsageRecordManager(models.Manager):
    def create_aggregate_obj(self, obj, type: str):
        """
        Create new BothUsageRecord object
        """
        # choose subscription type
        if type == 'voice':
            used_field = obj.seconds_used
        else:
            used_field = obj.kilobytes_used

        if obj.att_subscription_id:
            record = self.create(type_of_usage=type, subscription_id=obj.att_subscription_id.id,
                                 price=obj.price, usage_date=obj.usage_date.date(),
                                 used=used_field, type_of_subscription='att')
        else:
            record = self.create(type_of_usage=type, subscription_id=obj.sprint_subscription_id.id,
                                 price=obj.price, usage_date=obj.usage_date.date(),
                                 used=used_field, type_of_subscription='sprint')

        return record


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
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    usage_date = models.DateField(null=False)
    used = models.IntegerField(null=False)

    objects = BothUsageRecordManager()
