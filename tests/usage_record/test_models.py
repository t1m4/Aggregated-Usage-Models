from datetime import datetime, timedelta

import pytest
import pytz

from tests.subscription.factories import SubscriptionFactory
from tests.usage_record.factories import DataUsageRecordFactory, VoiceUsageRecordFactory
from wingtel.usage import models

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "record_type,factory_record_class",
    [
        (models.UsageRecord.USAGE_TYPES.data, DataUsageRecordFactory),
        (models.UsageRecord.USAGE_TYPES.voice, VoiceUsageRecordFactory),
    ],
)
def test_create_one_usage_record(record_type: str, factory_record_class):
    record = factory_record_class.create()
    usage_record = models.UsageRecord.objects.all().first()
    assert usage_record
    assert usage_record.type_of_usage == record_type
    assert usage_record.subscription == record.subscription_id
    assert usage_record.price == record.price
    assert (
        usage_record.used == record.kilobytes_used
        if record_type == models.UsageRecord.USAGE_TYPES.data
        else record.seconds_used
    )


@pytest.mark.parametrize(
    "record_type,factory_record_class",
    [
        (models.UsageRecord.USAGE_TYPES.data, DataUsageRecordFactory),
        (models.UsageRecord.USAGE_TYPES.voice, VoiceUsageRecordFactory),
    ],
)
def test_create_two_usage_records(record_type: str, factory_record_class):
    first_record = factory_record_class.create()
    second_record = factory_record_class.create(subscription_id=first_record.subscription_id)
    usage_record = models.UsageRecord.objects.all().first()
    assert usage_record
    assert usage_record.type_of_usage == record_type
    assert usage_record.subscription == first_record.subscription_id == second_record.subscription_id
    assert usage_record.price == (first_record.price + second_record.price)
    if record_type == models.UsageRecord.USAGE_TYPES.data:
        assert usage_record.used == (first_record.kilobytes_used + second_record.kilobytes_used)
    else:
        assert usage_record.used == (first_record.seconds_used + second_record.seconds_used)


def test_create_different_types_usage_records():
    """Create usage records with different types"""
    data_record = DataUsageRecordFactory.create()
    voice_record = VoiceUsageRecordFactory.create()
    data_usage_record = models.UsageRecord.objects.filter(type_of_usage=models.UsageRecord.USAGE_TYPES.data).first()
    voice_usage_record = models.UsageRecord.objects.filter(type_of_usage=models.UsageRecord.USAGE_TYPES.voice).first()
    assert data_usage_record
    assert voice_usage_record
    assert data_usage_record.subscription == data_record.subscription_id
    assert data_usage_record.price == data_record.price
    assert data_usage_record.used == data_record.kilobytes_used
    assert voice_usage_record.subscription == voice_record.subscription_id
    assert voice_usage_record.price == voice_record.price
    assert voice_usage_record.used == voice_record.seconds_used


def test_create_different_subscription_usage_records():
    """Create usage records with different subscription ids"""
    first_subscription = SubscriptionFactory.create()
    second_subscription = SubscriptionFactory.create(user=first_subscription.user)
    first_record = DataUsageRecordFactory.create(subscription_id=first_subscription)
    second_record = DataUsageRecordFactory.create(subscription_id=second_subscription)
    first_data_usage_record = models.UsageRecord.objects.filter(subscription=first_subscription).first()
    second_data_usage_record = models.UsageRecord.objects.filter(subscription=second_subscription).first()
    assert first_data_usage_record
    assert second_data_usage_record
    assert first_data_usage_record.subscription == first_record.subscription_id
    assert first_data_usage_record.price == first_record.price
    assert first_data_usage_record.used == first_record.kilobytes_used
    assert second_data_usage_record.subscription == second_record.subscription_id
    assert second_data_usage_record.price == second_record.price
    assert second_data_usage_record.used == second_record.kilobytes_used


def test_create_different_usage_date_usage_records():
    """Create usage records with different usage date"""
    today = datetime.now(pytz.utc)
    yesterday = today - timedelta(days=1)
    first_record = DataUsageRecordFactory.create(usage_date=today)
    second_record = DataUsageRecordFactory.create(usage_date=yesterday)
    first_data_usage_record = models.UsageRecord.objects.filter(usage_date=today).first()
    second_data_usage_record = models.UsageRecord.objects.filter(usage_date=yesterday).first()
    assert first_data_usage_record
    assert second_data_usage_record
    assert first_data_usage_record.subscription == first_record.subscription_id
    assert first_data_usage_record.price == first_record.price
    assert first_data_usage_record.used == first_record.kilobytes_used
    assert second_data_usage_record.subscription == second_record.subscription_id
    assert second_data_usage_record.price == second_record.price
    assert second_data_usage_record.used == second_record.kilobytes_used


@pytest.mark.parametrize(
    "record_type,factory_record_class,price_update,used_update",
    [
        (models.UsageRecord.USAGE_TYPES.data, DataUsageRecordFactory, -100, 100),
        (models.UsageRecord.USAGE_TYPES.voice, VoiceUsageRecordFactory, -100, -100),
    ],
)
def test_update_one_usage_record(record_type: str, factory_record_class, price_update: int, used_update: int):
    record = factory_record_class.create()

    record.price += price_update
    if record_type == models.UsageRecord.USAGE_TYPES.data:
        record.kilobytes_used += used_update
        new_fields = ["kilobytes_used"]
    else:
        record.seconds_used += used_update
        new_fields = ["seconds_used"]
    record.save(update_fields=["price"] + new_fields)
    usage_record = models.UsageRecord.objects.all().first()
    assert usage_record
    assert usage_record.type_of_usage == record_type
    assert usage_record.subscription == record.subscription_id
    assert usage_record.price == record.price
    assert (
        usage_record.used == record.kilobytes_used
        if record_type == models.UsageRecord.USAGE_TYPES.data
        else record.seconds_used
    )


@pytest.mark.parametrize(
    "record_type,factory_record_class",
    [
        (models.UsageRecord.USAGE_TYPES.data, DataUsageRecordFactory),
        (models.UsageRecord.USAGE_TYPES.voice, VoiceUsageRecordFactory),
    ],
)
def test_delete_one_usage_record(record_type: str, factory_record_class):
    record = factory_record_class.create()
    record.delete()
    usage_record = models.UsageRecord.objects.all().first()
    assert factory_record_class._meta.model.objects.all().count() == 0
    assert usage_record
    assert usage_record.price == 0
    assert usage_record.used == 0
