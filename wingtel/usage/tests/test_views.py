from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from django.urls import reverse

from wingtel.usage.models import BothUsageRecord
from wingtel.usage.tests.fill_models import fill_models, create_subscriptions


class TestSubscriptionExceededPrice(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        setup data for whole class
        """
        cls.price_limit_url = reverse('usage-price_limit')
        cls.params = {'price_limit': 1000, 'type_of_subscription': 'att', 'type_of_usage': 'data'}
        user = User.objects.create(username='test', password='test')
        create_subscriptions(user, count=4)
        fill_models(count=2)


    def test_cannot_get_without_params(self):
        response = self.client.get(self.price_limit_url)
        assert response.status_code == 400

    def test_cannot_get_without_price_limit(self):
        params = self.params.copy()
        del params['price_limit']
        response = self.client.get(self.price_limit_url, params)
        assert response.status_code == 400

    def test_cannot_get_with_invalid_price_limit(self):
        params = self.params.copy()
        params['price_limit'] = 'invalid'
        response = self.client.get(self.price_limit_url, params)
        assert response.status_code == 400

    def test_cannot_get_with_not_positive_price_limit(self):
        params = self.params.copy()
        params['price_limit'] = -1
        response = self.client.get(self.price_limit_url, params)
        assert response.status_code == 400

    def test_cannot_get_with_invalid_sub_type(self):
        params = self.params.copy()
        params['type_of_subscription'] = 'invalid'
        response = self.client.get(self.price_limit_url, params)
        assert response.status_code == 400

    def test_cannot_get_with_invalid_type_of_usage(self):
        params = self.params.copy()
        params['type_of_usage'] = 'invalid'
        response = self.client.get(self.price_limit_url, params)
        assert response.status_code == 400

    def test_can_get_only_with_limit_price(self):
        response = self.client.get(self.price_limit_url, {'price_limit': 1000})
        assert response.status_code == 200

    def test_can_get_with_params(self):
        response = self.client.get(self.price_limit_url, self.params)
        assert response.status_code == 200
        assert len(response.json()) == 4

    def test_can_get_with_sub_type_sprint(self):
        params = self.params.copy()
        params['type_of_subscription'] = 'sprint'
        response = self.client.get(self.price_limit_url, self.params)
        assert response.status_code == 200
        print(BothUsageRecord.objects.all().count())
        assert len(response.json()) == 4


# class TestUsageMetrics(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         """
#         setup data for whole class
#         """
#         cls.usage_metrics_url = reverse('usage-metrics', args=[10])
#         cls.aggregate_url = reverse('usage-aggregate')
#         cls.params = {'price_limit': 100, 'sub_type': 'att'}
#         user = User.objects.create(username='test', password='test')
#         create_subscriptions(user)
#         fill_models(count=2)
#
#     def setUp(self):
#         self.client.get(self.aggregate_url, {'type': 'data'})
#         self.client.get(self.aggregate_url, {'type': 'voice'})
#         self.params = {'from': '2019-1-1', 'to': '2019-1-2', 'usage_type': 'data', 'sub_type': 'att'}
#
#     def test_cannot_get_without_params(self):
#         response = self.client.get(self.usage_metrics_url)
#         assert response.status_code == 404
#
#     def test_cannot_get_without_from(self):
#         params = self.params.copy()
#         del params['from']
#         response = self.client.get(self.usage_metrics_url, params)
#         assert response.status_code == 404
#
#     def test_cannot_get_without_to(self):
#         params = self.params.copy()
#         del params['to']
#         response = self.client.get(self.usage_metrics_url, params)
#         assert response.status_code == 404
#
#     def test_cannot_get_without_usage_type(self):
#         params = self.params.copy()
#         del params['usage_type']
#         response = self.client.get(self.usage_metrics_url, params)
#         assert response.status_code == 404
#
#     def test_cannot_get_without_sub_type(self):
#         params = self.params.copy()
#         del params['sub_type']
#         response = self.client.get(self.usage_metrics_url, params)
#         assert response.status_code == 404
#
#     def test_cannot_get_with_invalid_from(self):
#         params = self.params.copy()
#         params['from'] = "invalid"
#         response = self.client.get(self.usage_metrics_url, params)
#         assert response.status_code == 404
#
#     def test_cannot_get_with_invalid_to(self):
#         params = self.params.copy()
#         params['to'] = "invalid"
#         response = self.client.get(self.usage_metrics_url, params)
#         assert response.status_code == 404
#
#     def test_cannot_get_with_invalid_usage_type(self):
#         params = self.params.copy()
#         params['usage_type'] = "invalid"
#         response = self.client.get(self.usage_metrics_url, params)
#         assert response.status_code == 404
#
#     def test_cannot_get_with_invalid_sub_type(self):
#         params = self.params.copy()
#         params['sub_type'] = "invalid"
#         response = self.client.get(self.usage_metrics_url, params)
#         assert response.status_code == 404
#
#     def test_can_get_with_params(self):
#         response = self.client.get(self.usage_metrics_url, self.params)
#         assert len(response.json()) == 3
#         assert response.status_code == 200
#
#     def test_get_empty_response_with_not_exits_subscription(self):
#         usage_metrics_url = reverse('usage-metrics', args=[100])
#         response = self.client.get(usage_metrics_url, self.params)
#         assert response.json() == []
#         assert response.status_code == 200
