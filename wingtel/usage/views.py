# Create your views here.
from django.db.models import Count, DateField, Sum, Q, F
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
        type = request.GET.get('type')
        model = self.models.get(type)
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)
        used_field = self.models_field[type]['used']
        result = model.objects.values(
            'att_subscription_id',
            day=TruncDay('usage_date', output_field=DateField()),
        ).annotate(
            att_count=Count('att_subscription_id'),
            total_price=Sum('price'),
            total_used=Sum(used_field),
        ).order_by('day')

        # self.create_bulk(result, type)
        return Response(result)

    def create_bulk(self, queryset, type):
        data_objects = []
        for row in queryset:
            obj = BothUsageRecord(type_of_usage=type, subscription_id=row['att_subscription_id'],
                                  price=row['total_price'], usage_date=row['day'],
                                  used=row['total_used'])
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
