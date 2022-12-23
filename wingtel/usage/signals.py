from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from wingtel.usage.models import DataUsageRecord, UsageRecord, VoiceUsageRecord
from wingtel.usage.services import (
    CreateUpdateUsageRecordService,
    DeleteUsageRecordService,
)


@receiver(pre_save, sender=DataUsageRecord, dispatch_uid="data_usage_save_handler")
def date_usage_handler(instance, **kwargs):
    service = CreateUpdateUsageRecordService(instance, UsageRecord.USAGE_TYPES.data)
    service.aggregate_object()


@receiver(pre_save, sender=VoiceUsageRecord, dispatch_uid="voice_usage_save_handler")
def voice_usage_handler(instance, **kwargs):
    service = CreateUpdateUsageRecordService(instance, UsageRecord.USAGE_TYPES.voice)
    service.aggregate_object()


@receiver(pre_delete, sender=DataUsageRecord, dispatch_uid="data_usage_delete_handler")
def date_usage_delete_handler(instance, **kwargs):
    service = DeleteUsageRecordService(instance, UsageRecord.USAGE_TYPES.data)
    service.modify_aggregated_object()


@receiver(pre_delete, sender=VoiceUsageRecord, dispatch_uid="voice_usage_delete_handler")
def voice_usage_delete_handler(instance, **kwargs):
    service = DeleteUsageRecordService(instance, UsageRecord.USAGE_TYPES.voice)
    service.modify_aggregated_object()
