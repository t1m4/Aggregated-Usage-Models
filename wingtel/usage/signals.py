from django.db.models.signals import post_save
from django.dispatch import receiver

from wingtel.usage.models import DataUsageRecord, BothUsageRecord, VoiceUsageRecord
from wingtel.usage.utils import get_object_or_none


@receiver(post_save, sender=DataUsageRecord, dispatch_uid="data_usage_handler")
def date_usage_handler(instance, **kwargs):
    record_type = BothUsageRecord.USAGE_TYPES.data
    aggregate_object(instance, record_type)


@receiver(post_save, sender=VoiceUsageRecord, dispatch_uid="voice_usage_handler")
def voice_usage_handler(instance, **kwargs):
    record_type = BothUsageRecord.USAGE_TYPES.voice
    aggregate_object(instance, record_type)


def aggregate_object(instance, record_type: str):
    """
    Create/Update an aggregate object using new instance
    """
    # check exist entry with this params

    if instance.att_subscription_id:
        fields = {
            'subscription_id': instance.att_subscription_id.id,
            'type_of_subscription': 'att'
        }
    else:
        fields = {
            'subscription_id': instance.sprint_subscription_id.id,
            'type_of_subscription': 'sprint'
        }
    fields['usage_date'] = instance.usage_date.date()
    fields['type_of_usage'] = record_type

    record = get_object_or_none(BothUsageRecord, **fields)
    if record:
        update_aggregate_object(record, instance, type=record_type)
    else:
        create_aggregate_object(instance, fields, type=record_type)


def update_aggregate_object(old_object, instance, type: str):
    """
    Update price and used
    """
    used_field = get_used_field(instance, type)
    old_object.price += instance.price
    old_object.used += used_field
    old_object.save(update_fields=['price', 'used'])


def create_aggregate_object(instance, fields: dict, type: str):
    """
    Create new BothUsageRecord object
    """
    used_field = get_used_field(instance, type)
    BothUsageRecord.objects.create(price=instance.price, used=used_field, **fields)


def get_used_field(instance, type: str):
    """
    Choose used based on type
    """
    if type == BothUsageRecord.USAGE_TYPES.data:
        used_field = instance.kilobytes_used
    else:
        used_field = instance.seconds_used
    return used_field


def ready():
    post_save.connect(date_usage_handler, sender=DataUsageRecord, dispatch_uid='data_usage_handler')
    post_save.connect(voice_usage_handler, sender=VoiceUsageRecord, dispatch_uid='voice_usage_handler')
