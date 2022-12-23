import datetime

import pytz
from factory import SubFactory, fuzzy
from factory.django import DjangoModelFactory

from tests.subscription.factories import SubscriptionFactory
from wingtel.usage import models


class DataUsageRecordFactory(DjangoModelFactory):
    usage_date = fuzzy.FuzzyDateTime(datetime.datetime.now(tz=pytz.utc))
    kilobytes_used = fuzzy.FuzzyInteger(0, 1000)

    class Meta:
        model = models.DataUsageRecord


class VoiceUsageRecordFactory(DjangoModelFactory):
    usage_date = fuzzy.FuzzyDateTime(datetime.datetime.now(tz=pytz.utc))
    seconds_used = fuzzy.FuzzyInteger(0, 1000)

    class Meta:
        model = models.VoiceUsageRecord


class UsageRecordFactory(DjangoModelFactory):
    subscription_id = SubFactory(SubscriptionFactory)
    type_of_usage = models.UsageRecord.USAGE_TYPES.data
    usage_date = fuzzy.FuzzyDateTime(datetime.datetime.now(tz=pytz.utc))
    used = fuzzy.FuzzyInteger(0, 1000)

    class Meta:
        model = models.UsageRecord
