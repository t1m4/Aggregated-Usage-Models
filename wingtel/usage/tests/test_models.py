from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import make_aware

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.sprint_subscriptions.models import SprintSubscription
from wingtel.usage.models import VoiceUsageRecord, DataUsageRecord, BothUsageRecord
from wingtel.usage.tests.fill_models import create_subscriptions
from wingtel.usage.utils import get_object_or_none


class TestDataUsageRecordModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        setup data for whole class
        """
        user = User.objects.create(username='test', password='test')
        create_subscriptions(user, count=4)
        cls.data_fields = {
            'price': 250,
            'usage_date': make_aware(datetime.now()),
            'kilobytes_used': 100,
        }
        cls.voice_fields = {
            'price': 250,
            'usage_date': make_aware(datetime.now()),
            'seconds_used': 100,
        }

    def test_can_create_aggregate_object_with_att_type(self):
        obj_subscription_id = 1
        obj = DataUsageRecord.objects.create(att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
                                             **self.data_fields)
        aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                           usage_date=obj.usage_date.date(), type_of_usage='data',
                                           type_of_subscription='att')
        assert aggregate_obj
        assert aggregate_obj.price == obj.price
        assert aggregate_obj.used == obj.kilobytes_used

    def test_can_create_aggregate_object_with_sprint_type(self):
        obj_subscription_id = 1
        obj = DataUsageRecord.objects.create(
            sprint_subscription_id=SprintSubscription.objects.get(pk=obj_subscription_id), **self.data_fields)
        aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                           usage_date=obj.usage_date.date(), type_of_usage='data',
                                           type_of_subscription='sprint')
        assert aggregate_obj
        assert aggregate_obj.price == obj.price
        assert aggregate_obj.used == obj.kilobytes_used

    def test_can_update_aggregate_object_with_att_type(self):
        count = 3
        data_fields = self.data_fields.copy()
        obj_subscription_id = 1
        full_price = 0
        full_used = 0

        for i in range(1, count + 1):
            data_fields['price'] = self.data_fields['price'] * i
            data_fields['kilobytes_used'] = self.data_fields['kilobytes_used'] * i
            obj = DataUsageRecord.objects.create(
                att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
                **data_fields)
            full_price += data_fields['price']
            full_used += data_fields['kilobytes_used']

        aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                           usage_date=data_fields['usage_date'].date(), type_of_usage='data',
                                           type_of_subscription='att')

        assert aggregate_obj
        assert aggregate_obj.price == full_price
        assert aggregate_obj.used == full_used

    def test_can_update_aggregate_object_with_sprint_type(self):
        count = 3
        data_fields = self.data_fields.copy()
        obj_subscription_id = 1
        full_price = 0
        full_used = 0

        for i in range(1, count + 1):
            data_fields['price'] = self.data_fields['price'] * i
            data_fields['kilobytes_used'] = self.data_fields['kilobytes_used'] * i
            obj = DataUsageRecord.objects.create(
                sprint_subscription_id=SprintSubscription.objects.get(pk=obj_subscription_id),
                **data_fields)
            full_price += data_fields['price']
            full_used += data_fields['kilobytes_used']

        aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                           usage_date=data_fields['usage_date'].date(), type_of_usage='data',
                                           type_of_subscription='sprint')

        assert aggregate_obj
        assert aggregate_obj.price == full_price
        assert aggregate_obj.used == full_used

    def test_can_create_different_aggregate_object_with_sub_type(self):
        data_fields = self.data_fields.copy()
        obj_subscription_id = 1

        att_obj = DataUsageRecord.objects.create(
            att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
            **data_fields)

        sprint_obj = DataUsageRecord.objects.create(
            sprint_subscription_id=SprintSubscription.objects.get(pk=obj_subscription_id),
            **data_fields)

        att_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                               usage_date=data_fields['usage_date'].date(), type_of_usage='data',
                                               type_of_subscription='att')
        assert att_aggregate_obj
        assert att_aggregate_obj.price == att_obj.price
        assert att_aggregate_obj.used == att_obj.kilobytes_used

        sprint_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                                  usage_date=data_fields['usage_date'].date(), type_of_usage='data',
                                                  type_of_subscription='sprint')
        assert sprint_aggregate_obj
        assert sprint_aggregate_obj.price == sprint_obj.price
        assert sprint_aggregate_obj.used == sprint_obj.kilobytes_used

    def test_can_create_different_aggregate_object_with_subscription_id(self):
        data_fields = self.data_fields.copy()
        first_obj_subscription_id = 1
        second_obj_subscription_id = 2

        first_obj = DataUsageRecord.objects.create(
            att_subscription_id=ATTSubscription.objects.get(pk=first_obj_subscription_id),
            **data_fields)

        second_obj = DataUsageRecord.objects.create(
            att_subscription_id=ATTSubscription.objects.get(pk=second_obj_subscription_id),
            **data_fields)

        first_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=first_obj_subscription_id,
                                                 usage_date=data_fields['usage_date'].date(), type_of_usage='data',
                                                 type_of_subscription='att')
        assert first_aggregate_obj
        assert first_aggregate_obj.price == first_obj.price
        assert first_aggregate_obj.used == first_obj.kilobytes_used

        second_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=second_obj_subscription_id,
                                                  usage_date=data_fields['usage_date'].date(), type_of_usage='data',
                                                  type_of_subscription='att')
        assert second_aggregate_obj
        assert second_aggregate_obj.price == second_obj.price
        assert second_aggregate_obj.used == second_obj.kilobytes_used

    def test_can_create_different_aggregate_object_with_usage_date(self):
        data_fields = self.data_fields.copy()
        first_data_fields = data_fields.copy()
        second_data_fields = data_fields.copy()
        second_data_fields['usage_date'] = make_aware(datetime.now() + timedelta(days=1))
        obj_subscription_id = 1

        first_obj = DataUsageRecord.objects.create(
            att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
            **first_data_fields)

        second_obj = DataUsageRecord.objects.create(
            att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
            **second_data_fields)

        first_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                                 usage_date=first_data_fields['usage_date'].date(),
                                                 type_of_usage='data',
                                                 type_of_subscription='att')

        second_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                                  usage_date=second_data_fields['usage_date'].date(),
                                                  type_of_usage='data',
                                                  type_of_subscription='att')
        assert first_aggregate_obj
        assert first_aggregate_obj.price == first_obj.price
        assert first_aggregate_obj.used == first_obj.kilobytes_used

        assert second_aggregate_obj
        assert second_aggregate_obj.price == second_obj.price
        assert second_aggregate_obj.used == second_obj.kilobytes_used


class TestVoiceUsageRecordModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        setup data for whole class
        """
        user = User.objects.create(username='test', password='test')
        create_subscriptions(user, count=4)
        # here
        cls.voice_fields = {
            'price': 250,
            'usage_date': make_aware(datetime.now()),
            'seconds_used': 100,
        }

        cls.model = VoiceUsageRecord
        cls.type_of_usage = 'voice'
        cls.obj_subscription_id = 5

    def test_can_create_aggregate_object_with_att_type(self):
        obj_subscription_id = self.obj_subscription_id
        obj = self.model.objects.create(att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
                                        **self.voice_fields)
        aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                           usage_date=obj.usage_date.date(), type_of_usage=self.type_of_usage,
                                           type_of_subscription='att')
        assert aggregate_obj
        assert aggregate_obj.price == obj.price
        assert aggregate_obj.used == obj.seconds_used

    def test_can_create_aggregate_object_with_sprint_type(self):
        obj_subscription_id = self.obj_subscription_id
        obj = self.model.objects.create(sprint_subscription_id=SprintSubscription.objects.get(pk=obj_subscription_id),
                                        **self.voice_fields)
        aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                           usage_date=obj.usage_date.date(), type_of_usage=self.type_of_usage,
                                           type_of_subscription='sprint')
        assert aggregate_obj
        assert aggregate_obj.price == obj.price
        assert aggregate_obj.used == obj.seconds_used

    def test_can_update_aggregate_object_with_att_type(self):
        count = 3
        data_fields = self.voice_fields.copy()
        obj_subscription_id = self.obj_subscription_id
        full_price = 0
        full_used = 0

        for i in range(1, count + 1):
            data_fields['price'] = self.voice_fields['price'] * i
            data_fields['seconds_used'] = self.voice_fields['seconds_used'] * i
            obj = self.model.objects.create(att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
                                            **data_fields)
            full_price += data_fields['price']
            full_used += data_fields['seconds_used']

        aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                           usage_date=data_fields['usage_date'].date(),
                                           type_of_usage=self.type_of_usage,
                                           type_of_subscription='att')

        assert aggregate_obj
        assert aggregate_obj.price == full_price
        assert aggregate_obj.used == full_used

    def test_can_update_aggregate_object_with_sprint_type(self):
        count = 3
        data_fields = self.voice_fields.copy()
        obj_subscription_id = self.obj_subscription_id
        full_price = 0
        full_used = 0

        for i in range(1, count + 1):
            data_fields['price'] = self.voice_fields['price'] * i
            data_fields['seconds_used'] = self.voice_fields['seconds_used'] * i
            obj = self.model.objects.create(
                sprint_subscription_id=SprintSubscription.objects.get(pk=obj_subscription_id),
                **data_fields)
            full_price += data_fields['price']
            full_used += data_fields['seconds_used']

        aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                           usage_date=data_fields['usage_date'].date(),
                                           type_of_usage=self.type_of_usage,
                                           type_of_subscription='sprint')

        assert aggregate_obj
        assert aggregate_obj.price == full_price
        assert aggregate_obj.used == full_used

    def test_can_create_different_aggregate_object_with_sub_type(self):
        data_fields = self.voice_fields.copy()
        obj_subscription_id = self.obj_subscription_id

        att_obj = self.model.objects.create(att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
                                            **data_fields)

        sprint_obj = self.model.objects.create(
            sprint_subscription_id=SprintSubscription.objects.get(pk=obj_subscription_id),
            **data_fields)

        att_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                               usage_date=data_fields['usage_date'].date(),
                                               type_of_usage=self.type_of_usage,
                                               type_of_subscription='att')
        assert att_aggregate_obj
        assert att_aggregate_obj.price == att_obj.price
        assert att_aggregate_obj.used == att_obj.seconds_used

        sprint_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                                  usage_date=data_fields['usage_date'].date(),
                                                  type_of_usage=self.type_of_usage,
                                                  type_of_subscription='sprint')
        assert sprint_aggregate_obj
        assert sprint_aggregate_obj.price == sprint_obj.price
        assert sprint_aggregate_obj.used == sprint_obj.seconds_used

    def test_can_create_different_aggregate_object_with_subscription_id(self):
        data_fields = self.voice_fields.copy()
        first_obj_subscription_id = self.obj_subscription_id
        second_obj_subscription_id = first_obj_subscription_id + 1

        first_obj = self.model.objects.create(
            att_subscription_id=ATTSubscription.objects.get(pk=first_obj_subscription_id),
            **data_fields)

        second_obj = self.model.objects.create(
            att_subscription_id=ATTSubscription.objects.get(pk=second_obj_subscription_id),
            **data_fields)

        first_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=first_obj_subscription_id,
                                                 usage_date=data_fields['usage_date'].date(),
                                                 type_of_usage=self.type_of_usage,
                                                 type_of_subscription='att')
        assert first_aggregate_obj
        assert first_aggregate_obj.price == first_obj.price
        assert first_aggregate_obj.used == first_obj.seconds_used

        second_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=second_obj_subscription_id,
                                                  usage_date=data_fields['usage_date'].date(),
                                                  type_of_usage=self.type_of_usage,
                                                  type_of_subscription='att')
        assert second_aggregate_obj
        assert second_aggregate_obj.price == second_obj.price
        assert second_aggregate_obj.used == second_obj.seconds_used

    def test_can_create_different_aggregate_object_with_usage_date(self):
        data_fields = self.voice_fields.copy()
        first_data_fields = data_fields.copy()
        second_data_fields = data_fields.copy()
        second_data_fields['usage_date'] = make_aware(datetime.now() + timedelta(days=1))
        obj_subscription_id = self.obj_subscription_id

        first_obj = self.model.objects.create(att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
                                              **first_data_fields)

        second_obj = self.model.objects.create(att_subscription_id=ATTSubscription.objects.get(pk=obj_subscription_id),
                                               **second_data_fields)

        first_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                                 usage_date=first_data_fields['usage_date'].date(),
                                                 type_of_usage=self.type_of_usage,
                                                 type_of_subscription='att')

        second_aggregate_obj = get_object_or_none(BothUsageRecord, subscription_id=obj_subscription_id,
                                                  usage_date=second_data_fields['usage_date'].date(),
                                                  type_of_usage=self.type_of_usage,
                                                  type_of_subscription='att')
        assert first_aggregate_obj
        assert first_aggregate_obj.price == first_obj.price
        assert first_aggregate_obj.used == first_obj.seconds_used

        assert second_aggregate_obj
        assert second_aggregate_obj.price == second_obj.price
        assert second_aggregate_obj.used == second_obj.seconds_used
