from typing import Dict, Union

from django.db import transaction

from wingtel.usage.models import DataUsageRecord, UsageRecord, VoiceUsageRecord
from wingtel.usage.utils import get_object_or_none


class CreateUpdateUsageRecordService:
    def __init__(self, new_instance: Union[DataUsageRecord, VoiceUsageRecord], record_type: str) -> None:
        self.new_instance = new_instance
        self.record_type = record_type
        self.old_instance = None
        if new_instance.id:
            # old instance exist only in update process
            self.old_instance = get_object_or_none(new_instance.__class__, id=new_instance.id)

    @transaction.atomic
    def aggregate_object(self):
        """Create/Update an aggregate object using new instance"""
        fields = {
            "type_of_usage": self.record_type,
            "subscription": self.new_instance.subscription_id,
            "usage_date": self.new_instance.usage_date.date(),
        }

        aggregated_instance = get_object_or_none(UsageRecord, **fields)
        if aggregated_instance:
            self.__update_aggregated_object(aggregated_instance)
        else:
            self.__create_aggregated_object(fields)

    def __create_aggregated_object(self, fields: Dict):
        """Create new UsageRecord object"""
        used_field = self.__get_used_field()
        UsageRecord.objects.create(price=self.new_instance.price, used=used_field, **fields)

    def __update_aggregated_object(self, aggregated_instance: UsageRecord):
        """Update existing UsageRecord object"""
        if self.old_instance:
            self.__reduce_old_object_fields(aggregated_instance)
        aggregated_instance.price += self.new_instance.price
        aggregated_instance.used += self.__get_used_field()
        aggregated_instance.save(update_fields=["price", "used"])

    def __get_used_field(self, instance=None):
        """Choose used field based on type"""
        if not instance:
            instance = self.new_instance
        if self.record_type == UsageRecord.USAGE_TYPES.data:
            used_field = instance.kilobytes_used
        else:
            used_field = instance.seconds_used
        return used_field

    def __reduce_old_object_fields(self, aggregated_instance: UsageRecord):
        """Delete self.old_instance fields from aggregated"""
        aggregated_instance.price -= self.old_instance.price
        aggregated_instance.used -= self.__get_used_field(self.old_instance)


class DeleteUsageRecordService:
    def __init__(self, instance: Union[DataUsageRecord, VoiceUsageRecord], record_type: str) -> None:
        self.instance = instance
        self.record_type = record_type

    def modify_aggregated_object(self):
        """Delete from aggregated object"""
        fields = {
            "type_of_usage": self.record_type,
            "subscription": self.instance.subscription_id,
            "usage_date": self.instance.usage_date.date(),
        }
        aggregated_instance = get_object_or_none(UsageRecord, **fields)
        if aggregated_instance:
            self.__reduce_values(aggregated_instance)
            aggregated_instance.save(update_fields=["price", "used"])

    def __reduce_values(self, aggregated_instance: UsageRecord):
        """Delete self.old_instance fields from aggregated"""
        aggregated_instance.price -= self.instance.price
        aggregated_instance.used -= self.__get_used_field()

    def __get_used_field(self):
        """Choose used field based on type"""
        if self.record_type == UsageRecord.USAGE_TYPES.data:
            used_field = self.instance.kilobytes_used
        else:
            used_field = self.instance.seconds_used
        return used_field
