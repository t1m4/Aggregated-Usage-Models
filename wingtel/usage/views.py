# Create your views here.
from datetime import datetime

import django_filters
from django.db.models import Count, DateField, Sum, QuerySet
from django.db.models.functions import TruncDay
from django.utils.timezone import make_aware
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from wingtel.usage.models import DataUsageRecord, BothUsageRecord, VoiceUsageRecord
from wingtel.usage.serializers import ExceededPriceSerializer


class SubscriptionExceededPrice(generics.ListAPIView):
    serializer_class = ExceededPriceSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['subscription_id', 'type_of_usage', 'type_of_subscription']

    def get_queryset(self):
        """
        Group by type_of_usage and subscription_id. Calculate price exceeded from given price_limit
        """
        try:
            price_limit = int(self.request.query_params.get('price_limit'))
        except (ValueError, TypeError):
            raise ValidationError(detail={'price_limit': ['This field must be an positive integer value.']})

        if price_limit <=0:
            raise ValidationError(detail={'price_limit': ['This field must be an positive integer value.']})

        result = BothUsageRecord.objects.filter().values(
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
        return result


class UsageMetrics(APIView):

    def get(self, request, id, *args, **kwargs):
        date_from = request.GET.get('from')
        date_to = request.GET.get('to')
        usage_type = request.GET.get('usage_type')
        usage_type_exist = BothUsageRecord.check_usage_type(usage_type)
        sub_type = request.GET.get('sub_type')
        sub_type_exist = BothUsageRecord.check_sub_type(sub_type)

        if not date_from or not date_to or not usage_type_exist or not sub_type_exist:
            return Response("You must provide from, to sub_type(att, sprint) and usage_type parameters",
                            status=status.HTTP_404_NOT_FOUND)

        date_format = "%Y-%m-%d"
        try:
            date_from = datetime.strptime(date_from, date_format).date()
            date_to = datetime.strptime(date_to, date_format).date()
        except ValueError:
            return Response("Use date format - {}".format(date_format), status=status.HTTP_404_NOT_FOUND)

        result = self.aggregate(id, usage_type, sub_type, date_from, date_to)

        return Response(result)

    def aggregate(self, id, usage_type: str, sub_type: str, date_from, date_to):
        """
        Group by subscription_id, aggregate price and used
        """
        query = BothUsageRecord.objects.filter(
            subscription_id=id,
            type_of_usage=usage_type,
            type_of_subscription=sub_type,
            usage_date__gte=date_from,
            usage_date__lte=date_to
        ).values(
            'subscription_id'
        ).annotate(
            total_price=Sum('price'),
            total_used=Sum('used'),
        ).values(
            'subscription_id',
            'total_price',
            'total_used'
        )
        if len(query) == 0:
            result = []
        else:
            result = query[0].items()
        return result
