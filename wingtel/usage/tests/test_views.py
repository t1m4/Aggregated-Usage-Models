from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from django.urls import reverse

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.sprint_subscriptions.models import SprintSubscription
from wingtel.usage.tests.fill_models import fill_models, create_subscription


class TestSubscriptionExceededPrice(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        setup data for whole class
        """
        cls.price_limit_url = reverse('usage-price_limit')
        cls.params = {'price_limit': 1000, 'type_of_subscription': 'att', 'type_of_usage': 'data'}
        user = User.objects.create(username='test', password='test')
        cls.att_subscriptions = create_subscription(user, ATTSubscription, 4)
        cls.sprint_subscriptions = create_subscription(user, SprintSubscription, 4)
        fill_models(cls.att_subscriptions[-1].id)

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

    def test_cannot_get_with_invalid_type_of_subscription(self):
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

    def test_can_get_with_type_of_subscription_sprint(self):
        params = self.params.copy()
        params['type_of_subscription'] = 'sprint'
        response = self.client.get(self.price_limit_url, self.params)
        assert response.status_code == 200
        assert len(response.json()) == 4


class TestUsageMetrics(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        setup data for whole class
        """
        cls.usage_metrics_url = reverse('usage-metrics', args=[15])
        user = User.objects.create(username='test', password='test')
        cls.att_subscriptions = create_subscription(user, ATTSubscription, 4)
        cls.sprint_subscriptions = create_subscription(user, SprintSubscription, 4)
        fill_models(cls.att_subscriptions[-1].id)

    def setUp(self):
        self.params = {'usage_date__gte': '2019-1-1', 'usage_date__lte': '2019-1-2', 'type_of_usage': 'data',
                       'type_of_subscription': 'att'}

    def test_can_get_without_params(self):
        response = self.client.get(self.usage_metrics_url)
        assert response.status_code == 200

    def test_cannot_get_without_invalid_usage_type(self):
        params = self.params.copy()
        params['type_of_usage'] = 'invalid'
        response = self.client.get(self.usage_metrics_url, params)
        assert response.status_code == 400

    def test_cannot_get_without_invalid_type_of_subscription(self):
        params = self.params.copy()
        params['type_of_subscription'] = 'invalid'
        response = self.client.get(self.usage_metrics_url, params)
        assert response.status_code == 400

    def test_cannot_get_without_invalid_usage_date__gte(self):
        params = self.params.copy()
        params['usage_date__gte'] = 'invalid'
        response = self.client.get(self.usage_metrics_url, params)
        assert response.status_code == 400

    def test_cannot_get_without_invalid_usage_date__lte(self):
        params = self.params.copy()
        params['usage_date__lte'] = 'invalid'
        response = self.client.get(self.usage_metrics_url, params)
        assert response.status_code == 400

    def test_get_empty_response_with_not_exits_subscription(self):
        usage_metrics_url = reverse('usage-metrics', args=[100])
        response = self.client.get(usage_metrics_url, self.params)
        assert response.json() == []
        assert response.status_code == 200
