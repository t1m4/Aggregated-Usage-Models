import datetime

import pytz
from factory import SubFactory, fuzzy
from factory.django import DjangoModelFactory

from tests.subscription.factories import SubscriptionFactory
from wingtel.usage import models


class DataUsageRecordFactory(DjangoModelFactory):
    subscription_id = SubFactory(SubscriptionFactory)
    usage_date = fuzzy.FuzzyDateTime(datetime.datetime.now(tz=pytz.utc))
    price = fuzzy.FuzzyInteger(0, 1000)
    kilobytes_used = fuzzy.FuzzyInteger(0, 1000)

    class Meta:
        model = models.DataUsageRecord


class VoiceUsageRecordFactory(DjangoModelFactory):
    subscription_id = SubFactory(SubscriptionFactory)
    usage_date = fuzzy.FuzzyDateTime(datetime.datetime.now(tz=pytz.utc))
    price = fuzzy.FuzzyInteger(0, 1000)
    seconds_used = fuzzy.FuzzyInteger(0, 1000)

    class Meta:
        model = models.VoiceUsageRecord


class UsageRecordFactory(DjangoModelFactory):
    subscription = SubFactory(SubscriptionFactory)
    type_of_usage = models.UsageRecord.USAGE_TYPES.data
    usage_date = fuzzy.FuzzyDateTime(datetime.datetime.now(tz=pytz.utc))
    price = fuzzy.FuzzyInteger(0, 1000)
    used = fuzzy.FuzzyInteger(0, 1000)

    class Meta:
        model = models.UsageRecordView
