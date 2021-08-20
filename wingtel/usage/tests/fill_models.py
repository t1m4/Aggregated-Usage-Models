import json
from datetime import datetime

from django.utils.timezone import make_aware

from wingtel.att_subscriptions.models import Subscription
from wingtel.settings import BASE_DIR
from wingtel.usage.models import VoiceUsageRecord, DataUsageRecord


def read_file(filename):
    with open(filename, 'r') as f:
        result = json.load(f)
    return result


def fill_models(id):
    """
    Create objects from fixtures.json
    """
    data = read_file(BASE_DIR + '/wingtel/usage/tests/fixtures.json')

    data_objects = []
    voice_objects = []
    # In different tests class ATTSubscription pk will be increase automatically
    # 4, 8, 12, 16
    # 0, 1, 2, 3
    # multiply = count * 4
    multiply = (id / 4 - 1) * 4

    k = 0
    for i in data:
        if k > 100 and k < 2000 or k > 2100 and k < 4000:
            k += 1
            continue
        # use each time different subscription
        fields = {
            'subscription_id': Subscription.objects.get(pk=i['fields']['subscription'] + multiply),
            'usage_date': make_aware(datetime.strptime(i['fields']['usage_date'], "%Y-%m-%dT%H:%M:%S.%fZ")),
            'price': int(float(i['fields']['price'])),
        }
        if i.get('model') == 'usage.datausagerecord':
            obj = DataUsageRecord.objects.create(**fields, kilobytes_used=i['fields']['kilobytes_used'])
            data_objects.append(obj)
        else:
            obj = VoiceUsageRecord.objects.create(**fields, seconds_used=i['fields']['seconds_used'])
            voice_objects.append(obj)
        k += 1



def create_subscription(user, subscription_class, count: int = 4):
    objects = []
    for index in range(count):
        objects.append(subscription_class(device_id=index, user=user))

    subscription_class.objects.bulk_create(objects)
    return objects
