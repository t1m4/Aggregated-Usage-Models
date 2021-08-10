# Create your views here.
from datetime import datetime

from django.db.models import Count, DateField, Sum
from django.db.models.functions import TruncDay
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from wingtel.usage.models import DataUsageRecord, BothUsageRecord, VoiceUsageRecord
from wingtel.usage.tests.fill_models import fill_models


class FillModel(APIView):
    def get(self, request, *args, **kwargs):
        fill_models()
        return Response('ok')


class AggregateDataView(APIView):
    models = {'data': DataUsageRecord, 'voice': VoiceUsageRecord}
    models_field = {'data': {'used': 'kilobytes_used'}, 'voice': {'used': 'seconds_used'}}

    def get(self, request, *args, **kwargs):
        date_from = request.GET.get('from')
        date_to = request.GET.get('to')

        if date_from and date_to:
            try:
                date_format = "%Y-%m-%d"
                date_from = datetime.strptime(date_from, date_format)
                date_to = datetime.strptime(date_to, date_format)
            except ValueError:
                return Response("Use date format - {}".format(date_format), status=status.HTTP_404_NOT_FOUND)

        type = request.GET.get('type', 'data')
        result = self.aggregate(type, date_from, date_to)

        self.create_bulk(result, type)
        return Response(result)

    def aggregate(self, type: str, date_from, date_to):
        """
        Filter Records by given date. Group by subscription_ids and day. Calculate total price and used.
        """
        model = self.models.get(type)
        used_field = self.models_field[type]['used']

        # Can aggregate data from date interval. For example from 2019-01-01 to 2019-01-08
        if date_from and date_to:
            date_filter_result = model.objects.filter(
                usage_date__gte=make_aware(date_from),
                usage_date__lte=make_aware(date_to)
            )
        else:
            date_filter_result = model.objects.filter()

        result = date_filter_result.values(
            'att_subscription_id',
            'sprint_subscription_id',
            day=TruncDay('usage_date', output_field=DateField()),
        ).annotate(
            att_count=Count('att_subscription_id'),
            sprint_count=Count('sprint_subscription_id'),
            total_price=Sum('price'),
            total_used=Sum(used_field),
        )
        return result

    def create_bulk(self, queryset, type):
        """
        Create BothUsageRecord using .bulk_create(). Divided data by subscription_id
        """
        data_objects = []
        for row in queryset:
            if row.get('att_subscription_id'):
                obj = BothUsageRecord(type_of_usage=type, subscription_id=row['att_subscription_id'],
                                      price=row['total_price'], usage_date=row['day'],
                                      used=row['total_used'], type_of_subscription='att')
            else:
                obj = BothUsageRecord(type_of_usage=type, subscription_id=row['sprint_subscription_id'],
                                      price=row['total_price'], usage_date=row['day'],
                                      used=row['total_used'], type_of_subscription='sprint')
            data_objects.append(obj)

        BothUsageRecord.objects.bulk_create(data_objects)


class SubscriptionExceededPrice(APIView):

    def get(self, request, *args, **kwargs):
        try:
            price_limit = int(request.GET.get('price_limit'))
        except (ValueError, TypeError):
            return Response(status=status.HTTP_404_NOT_FOUND)

        # check sub_type
        sub_type = request.GET.get('sub_type')
        sub_type_exist = BothUsageRecord.check_sub_type(sub_type)

        if not price_limit or not sub_type_exist:
            return Response("You must provide price_limit and sub_type(att, sprint) parameters",
                            status=status.HTTP_404_NOT_FOUND)

        result = self.aggregate(price_limit, sub_type)
        return Response(result)

    def aggregate(self, price_limit: int, sub_type: str):
        """
        Group by type_of_usage and subscription_id. Calculate price exceeded from given price_limit
        """
        result = BothUsageRecord.objects.filter(type_of_subscription=sub_type).values(
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

        # for each usage
        # result = BothUsageRecord.objects.filter(
        #     price__gt=price_limit, type_of_subscription=sub_type
        # ).annotate(
        #     price_exceeded=Sum('price') - price_limit
        # ).values(
        #     'type_of_usage',
        #     'subscription_id',
        #     'type_of_subscription',
        #     'price_exceeded',
        # )
        return result


class UsageMetrics(APIView):
    type_of_usage = ['data', 'voice']

    def get(self, request, id, *args, **kwargs):
        date_from = request.GET.get('from')
        date_to = request.GET.get('to')
        usage_type = request.GET.get('usage_type')
        sub_type = request.GET.get('sub_type')
        sub_type_exist = BothUsageRecord.check_sub_type(sub_type)

        if not date_from or not date_to or usage_type not in self.type_of_usage or not sub_type_exist:
            return Response("You must provide from, to sub_type(att, sprint) and usage_type parameters",
                            status=status.HTTP_404_NOT_FOUND)

        try:
            date_format = "%Y-%m-%d"
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
