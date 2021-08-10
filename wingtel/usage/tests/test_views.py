from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from django.urls import reverse

from wingtel.usage.models import BothUsageRecord
from wingtel.usage.tests.fill_models import fill_models, create_subscriptions


class TestAggregateDataView(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        setup data for whole class
        """
        cls.aggregate_url = reverse('usage-aggregate')
        user = User.objects.create(username='test', password='test')
        create_subscriptions(user)
        fill_models()

    def setUp(self):
        pass

    def test_can_aggregate_data(self):
        response = self.client.get(self.aggregate_url, params={'type': 'data'})
        assert len(response.json()) == BothUsageRecord.objects.all().count()

    def test_can_aggregate_without_type(self):
        response = self.client.get(self.aggregate_url)
        assert len(response.json()) == BothUsageRecord.objects.all().count()

    def test_can_aggregate_with_voice_type(self):
        response = self.client.get(self.aggregate_url, params={'type': 'voice'})
        assert len(response.json()) == BothUsageRecord.objects.all().count()
