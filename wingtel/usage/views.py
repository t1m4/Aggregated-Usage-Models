# Create your views here.
from datetime import datetime

from django.db.models import Count, DateField, Sum
from django.db.models.functions import TruncDay
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from wingtel.usage.fill_models import fill_models
from wingtel.usage.models import DataUsageRecord, BothUsageRecord, VoiceUsageRecord


class FillModel(APIView):
    def get(self, request, *args, **kwargs):
        fill_models()
        return Response('ok')


class AggregateDataView(APIView):
    models = {'data': DataUsageRecord, 'voice': VoiceUsageRecord}
    models_field = {'data': {'used': 'kilobytes_used'}, 'voice': {'used': 'seconds_used'}}

    def get(self, request, *args, **kwargs):
        type = request.GET.get('type', 'data')
        model = self.models.get(type)
        used_field = self.models_field[type]['used']
        result = model.objects.values(
            'att_subscription_id',
            'sprint_subscription_id',
            day=TruncDay('usage_date', output_field=DateField()),
        ).annotate(
            att_count=Count('att_subscription_id'),
            sprint_count=Count('sprint_subscription_id'),
            total_price=Sum('price'),
            total_used=Sum(used_field),
        ).order_by('day')
        print(len(result))
        self.create_bulk(result, type)
        return Response(result)

    def create_bulk(self, queryset, type):
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


class SubcsriptionExceededPrice(APIView):
    def get(self, request, *args, **kwargs):
        try:
            price_limit = int(request.GET.get('price_limit'))
        except ValueError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not price_limit:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # for usage group by id
        result = BothUsageRecord.objects.values(
            'type_of_usage',
            'subscription_id'
        ).annotate(
            total_price=Sum('price'),
            price_exceeded=Sum('price') - price_limit
        ).filter(
            total_price__gt=price_limit
        ).values(
            'type_of_usage',
            'subscription_id',
            'price_exceeded',
        )

        # for each usage
        # result = BothUsageRecord.objects.filter(
        #     price__gt=price_limit
        # ).annotate(
        #     price_exceeded=Sum('price') - price_limit
        # ).values(
        #     'type_of_usage',
        #     'subscription_id',
        #     'price_exceeded',
        # )

        return Response(result)


class UsageMetrics(APIView):
    type_of_usage = ['data', 'voice']

    def get(self, request, id, *args, **kwargs):
        date_from = request.GET.get('from')
        date_to = request.GET.get('to')
        type = request.GET.get('type')
        if not date_from or not date_to or type not in self.type_of_usage:
            return Response("You must provide from, to and type parameters", status=status.HTTP_404_NOT_FOUND)

        try:
            date_format = "%Y-%m-%d"
            date_from = datetime.strptime(date_from, date_format).date()
            date_to = datetime.strptime(date_to, date_format).date()
        except ValueError:
            return Response("Use date format - {}".format(date_format), status=status.HTTP_404_NOT_FOUND)

        query = BothUsageRecord.objects.filter(
            subscription_id=id,
            type_of_usage=type,
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

        result = []
        for row in query:
            result = row.items()
        return Response(result)
