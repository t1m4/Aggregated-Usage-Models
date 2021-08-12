from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import make_aware

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.sprint_subscriptions.models import SprintSubscription
from wingtel.usage.models import VoiceUsageRecord, DataUsageRecord, BothUsageRecord
from wingtel.usage.tests.fill_models import create_subscriptions, create_subscription
from wingtel.usage.utils import get_object_or_none


class TestUsageRecordModel:
    def test_can_create_aggregate_object_with_att_subscription_type(self):
        object = self.model.objects.create(att_subscription_id=self.att_subscriptions[0],
                                           **self.data_fields)
        aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=self.att_subscriptions[0].id,
                                              type_of_subscription='att',
                                              usage_date=object.usage_date.date(), type_of_usage=self.type_of_usage)
        assert aggregate_object
        assert aggregate_object.price == object.price
        assert aggregate_object.used == object.__dict__.get(self.used)

    def test_can_create_aggregate_object_with_sprint_subscription_type(self):
        object = self.model.objects.create(
            sprint_subscription_id=self.sprint_subscriptions[0], **self.data_fields)
        aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=self.sprint_subscriptions[0].id,
                                              type_of_subscription='sprint',
                                              usage_date=object.usage_date.date(), type_of_usage=self.type_of_usage)
        assert aggregate_object
        assert aggregate_object.price == object.price
        assert aggregate_object.used == object.__dict__.get(self.used)

    def test_can_update_aggregate_object_with_att_subscription_type(self):
        count = 3
        data_fields = self.data_fields.copy()
        total_price = 0
        total_used = 0

        for i in range(1, count + 1):
            data_fields['price'] = self.data_fields['price'] * i
            data_fields[self.used] = self.data_fields[self.used] * i
            self.model.objects.create(att_subscription_id=self.att_subscriptions[0], **data_fields)
            total_price += data_fields['price']
            total_used += data_fields[self.used]

        aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=self.att_subscriptions[0].id,
                                              usage_date=data_fields['usage_date'].date(),
                                              type_of_usage=self.type_of_usage,
                                              type_of_subscription='att')

        assert aggregate_object
        assert aggregate_object.price == total_price
        assert aggregate_object.used == total_used

    def test_can_update_aggregate_object_with_sprint_subscription_type(self):
        count = 3
        data_fields = self.data_fields.copy()
        total_price = 0
        total_used = 0

        for i in range(1, count + 1):
            data_fields['price'] = self.data_fields['price'] * i
            data_fields[self.used] = self.data_fields[self.used] * i
            self.model.objects.create(
                sprint_subscription_id=self.sprint_subscriptions[0],
                **data_fields)
            total_price += data_fields['price']
            total_used += data_fields[self.used]

        aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=self.sprint_subscriptions[0].id,
                                              usage_date=data_fields['usage_date'].date(),
                                              type_of_usage=self.type_of_usage,
                                              type_of_subscription='sprint')

        assert aggregate_object
        assert aggregate_object.price == total_price
        assert aggregate_object.used == total_used

    def test_can_create_different_aggregate_object_with_subscription_type(self):
        data_fields = self.data_fields.copy()

        att_object = self.model.objects.create(att_subscription_id=self.att_subscriptions[0], **data_fields)
        sprint_object = self.model.objects.create(sprint_subscription_id=self.sprint_subscriptions[0],
                                                  **data_fields)

        att_aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=self.att_subscriptions[0].id,
                                                  usage_date=data_fields['usage_date'].date(),
                                                  type_of_usage=self.type_of_usage,
                                                  type_of_subscription='att')
        sprint_aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=self.sprint_subscriptions[0].id,
                                                     usage_date=data_fields['usage_date'].date(),
                                                     type_of_usage=self.type_of_usage,
                                                     type_of_subscription='sprint')

        assert att_aggregate_object
        assert att_aggregate_object.price == att_object.price
        assert att_aggregate_object.used == att_object.__dict__.get(self.used)

        assert sprint_aggregate_object
        assert sprint_aggregate_object.price == sprint_object.price
        assert sprint_aggregate_object.used == sprint_object.__dict__.get(self.used)

    def test_can_create_different_aggregate_object_with_subscription_id(self):
        data_fields = self.data_fields.copy()

        first_object = self.model.objects.create(att_subscription_id=self.att_subscriptions[0], **data_fields)
        second_object = self.model.objects.create(att_subscription_id=self.att_subscriptions[1], **data_fields)

        first_aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=self.att_subscriptions[0].id,
                                                    usage_date=data_fields['usage_date'].date(),
                                                    type_of_usage=self.type_of_usage,
                                                    type_of_subscription='att')

        second_aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=self.att_subscriptions[1].id,
                                                     usage_date=data_fields['usage_date'].date(),
                                                     type_of_usage=self.type_of_usage,
                                                     type_of_subscription='att')
        assert first_aggregate_object
        assert first_aggregate_object.price == first_object.price
        assert first_aggregate_object.used == first_object.__dict__.get(self.used)

        assert second_aggregate_object
        assert second_aggregate_object.price == second_object.price
        assert second_aggregate_object.used == second_object.__dict__.get(self.used)

    def test_can_create_different_aggregate_object_with_usage_date(self):
        data_fields = self.data_fields.copy()
        first_data_fields = data_fields.copy()
        second_data_fields = data_fields.copy()
        second_data_fields['usage_date'] = make_aware(datetime.now() + timedelta(days=1))
        att_object = self.att_subscriptions[0]

        first_object = self.model.objects.create(att_subscription_id=att_object, **first_data_fields)
        second_object = self.model.objects.create(att_subscription_id=att_object, **second_data_fields)

        first_aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=att_object.id,
                                                    usage_date=first_data_fields['usage_date'].date(),
                                                    type_of_usage=self.type_of_usage,
                                                    type_of_subscription='att')

        second_aggregate_object = get_object_or_none(BothUsageRecord, subscription_id=att_object.id,
                                                     usage_date=second_data_fields['usage_date'].date(),
                                                     type_of_usage=self.type_of_usage,
                                                     type_of_subscription='att')

        assert first_aggregate_object
        assert first_aggregate_object.price == first_object.price
        assert first_aggregate_object.used == first_object.__dict__.get(self.used)

        assert second_aggregate_object
        assert second_aggregate_object.price == second_object.price
        assert second_aggregate_object.used == second_object.__dict__.get(self.used)


class TestDataUsageRecordModel(TestUsageRecordModel, TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        setup data for whole class
        """
        user = User.objects.create(username='test', password='test')
        cls.object_subscription_id = create_subscriptions(user, count=4)
        cls.data_fields = {
            'price': 250,
            'usage_date': make_aware(datetime.now()),
            'kilobytes_used': 100,
        }
        cls.att_subscriptions = create_subscription(user, ATTSubscription, 4)
        cls.sprint_subscriptions = create_subscription(user, SprintSubscription, 4)
        cls.model = DataUsageRecord
        cls.type_of_usage = 'data'
        cls.used = "kilobytes_used"


class TestVoiceUsageRecordModel(TestUsageRecordModel, TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        setup data for whole class
        """
        user = User.objects.create(username='test', password='test')
        cls.object_subscription_id = create_subscriptions(user, count=4)
        cls.data_fields = {
            'price': 250,
            'usage_date': make_aware(datetime.now()),
            'seconds_used': 100,
        }
        cls.att_subscriptions = create_subscription(user, ATTSubscription, 4)
        cls.sprint_subscriptions = create_subscription(user, SprintSubscription, 4)
        cls.model = VoiceUsageRecord
        cls.type_of_usage = 'voice'
        cls.used = "seconds_used"
