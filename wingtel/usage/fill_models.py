import json
from datetime import datetime

from django.utils.timezone import make_aware

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.settings import BASE_DIR
from wingtel.sprint_subscriptions.models import SprintSubscription
from wingtel.usage.models import VoiceUsageRecord, DataUsageRecord


def read_file(filename):
    with open(filename, 'r') as f:
        result = json.load(f)
    return result


def fill_models():
    """
    Create objects from fixtures.json
    """
    data = read_file(BASE_DIR + '/wingtel/usage/fixtures.json')

    data_objects = []
    voice_objects = []

    k = 0
    for i in data:
        # use each time different subscription
        if k % 2 == 0:
            subscription = {'att_subscription_id': ATTSubscription.objects.get(pk=i['fields']['subscription'])}
        else:
            subscription = {'sprint_subscription_id': SprintSubscription.objects.get(pk=i['fields']['subscription'])}
        usage_date = make_aware(datetime.strptime(i['fields']['usage_date'], "%Y-%m-%dT%H:%M:%S.%fZ"))

        if i.get('model') == 'usage.datausagerecord':
            obj = DataUsageRecord(**subscription, price=float(i['fields']['price']),
                                  kilobytes_used=i['fields']['kilobytes_used'], usage_date=usage_date)
            data_objects.append(obj)
        else:
            obj = VoiceUsageRecord(**subscription, price=float(i['fields']['price']),
                                   seconds_used=i['fields']['seconds_used'], usage_date=usage_date)
            voice_objects.append(obj)
        k += 1
        if k % 1000 == 0:
            print(k)
    DataUsageRecord.objects.bulk_create(data_objects)
    VoiceUsageRecord.objects.bulk_create(voice_objects)


if __name__ == '__main__':
    read_file('fixtures.json')
