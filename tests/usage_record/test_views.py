import pytest
from django.urls import reverse

from tests.usage_record.factories import UsageRecordFactory
from wingtel.usage.models import UsageRecord

pytestmark = pytest.mark.django_db
usage_price_limit_url = reverse("usage-price_limit")


class TestUsageRecordPriceLimitView:
    def test_view_with_empty_response(self, api_client):
        response = api_client.get(usage_price_limit_url, {"price_limit": 10})
        response_json = response.json()
        assert response_json == []

    def test_view_with_one_response(self, api_client):
        price = 10
        UsageRecordFactory.create(price=price)
        UsageRecordFactory.create(price=price + 10)
        response = api_client.get(usage_price_limit_url, {"price_limit": price + 5})
        response_json = response.json()

        assert UsageRecord.objects.all().count() == 2
        assert len(response_json) == 1
        record = response_json[0]
        assert record["price_exceeded"] == 5

    def test_view_with_filtering(self, api_client):
        price = 10
        UsageRecordFactory.create(price=price, type_of_usage=UsageRecord.USAGE_TYPES.data)
        UsageRecordFactory.create(price=price, type_of_usage=UsageRecord.USAGE_TYPES.voice)

        data_response = api_client.get(
            usage_price_limit_url, {"price_limit": price - 1, "type_of_usage": UsageRecord.USAGE_TYPES.data}
        )
        data_response_json = data_response.json()
        assert len(data_response_json) == 1
        record = data_response_json[0]
        assert record["price_exceeded"] == 1

        voice_response = api_client.get(
            usage_price_limit_url, {"price_limit": price - 1, "type_of_usage": UsageRecord.USAGE_TYPES.voice}
        )
        voice_response_json = voice_response.json()
        assert len(voice_response_json) == 1
        record = voice_response_json[0]
        assert record["price_exceeded"] == 1


class TestUsageRecordTotalMetricsView:
    def test_view_with_empty_response(self, api_client):
        usage_record = UsageRecordFactory.create()
        usage_metrics_url = reverse("usage-metrics", kwargs={"subscription_id": usage_record.subscription_id + 1})
        response = api_client.get(usage_metrics_url)
        response_json = response.json()
        assert response_json == []

    def test_view_with_two_response(self, api_client):
        usage_record = UsageRecordFactory.create()
        usage_metrics_url = reverse("usage-metrics", kwargs={"subscription_id": usage_record.subscription_id})
        response = api_client.get(usage_metrics_url)
        response_json = response.json()
        assert len(response_json) == 1
        record = response_json[0]
        assert record["subscription_id"] == usage_record.subscription_id
        assert record["total_price"] == usage_record.price
        assert record["total_used"] == usage_record.used
