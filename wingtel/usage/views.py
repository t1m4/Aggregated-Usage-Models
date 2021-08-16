# Create your views here.

import django_filters
from django.db.models import Sum
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from wingtel.usage.models import BothUsageRecord
from wingtel.usage.serializers import ExceededPriceSerializer, UsageMetricsSerilizer, PriceLimitDeserializer


class SubscriptionExceededPrice(generics.ListAPIView):
    serializer_class = ExceededPriceSerializer
    filterset_fields = ['subscription_id', 'type_of_usage', 'type_of_subscription']

    def get_queryset(self):
        """
        Group by type_of_usage and subscription_id. Calculate price exceeded from given price_limit
        """
        serializer = PriceLimitDeserializer(data={'price_limit': self.request.query_params.get('price_limit')})
        serializer.is_valid(raise_exception=True)
        price_limit = serializer.validated_data['price_limit']

        queryset = BothUsageRecord.objects.filter().values(
            'type_of_usage',
            'subscription_id'
        ).annotate(
            total_price=Sum('price'),
            price_exceeded=Sum('price') - price_limit
        ).filter(
            total_price__gt=price_limit
        ).values(
            'type_of_usage',
            'type_of_subscription',
            'subscription_id',
            'price_exceeded',
        )
        return queryset


class UsageMetricsGenericsView(generics.ListAPIView):
    serializer_class = UsageMetricsSerilizer
    filterset_fields = {'subscription_id': ['exact'], 'type_of_usage': ['exact'], 'type_of_subscription': ['exact'],
                        'usage_date': ['gte', 'lte']}

    def get_queryset(self):
        id = self.kwargs['id']
        queryset = BothUsageRecord.objects.filter(
            subscription_id=id,
        ).values(
            'subscription_id'
        ).annotate(
            total_price=Sum('price'),
            total_used=Sum('used'),
        )
        return queryset
