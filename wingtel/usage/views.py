from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from wingtel.usage.selectors import (
    get_usage_records_group_by_subscription_id,
    get_usage_records_with_exceeded_price,
)
from wingtel.usage.serializers import (
    PriceLimitDeserializer,
    UsageRecordExceedingPriceSerializer,
    UsageRecordTotalMetricsSerializer,
)


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        return Response("ok")


class UsageRecordPriceLimitView(generics.ListAPIView):
    serializer_class = UsageRecordExceedingPriceSerializer
    filterset_fields = ["subscription_id", "type_of_usage"]

    def get_queryset(self):
        """
        Group by type_of_usage and subscription_id. Calculate price exceeded from given price_limit
        """
        serializer = PriceLimitDeserializer(data={"price_limit": self.request.GET.get("price_limit")})
        serializer.is_valid(raise_exception=True)
        price_limit: int = serializer.validated_data["price_limit"]
        return get_usage_records_with_exceeded_price(price_limit)


class UsageRecordTotalMetricsView(generics.ListAPIView):
    serializer_class = UsageRecordTotalMetricsSerializer
    filterset_fields = {"type_of_usage": ["exact"], "usage_date": ["gte", "lte"]}

    def get_queryset(self):
        return get_usage_records_group_by_subscription_id(self.kwargs["subscription_id"])
