import json
from datetime import datetime

from django.utils.timezone import make_aware

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.settings import BASE_DIR
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
    for i in data:
        if i.get('model') == 'usage.datausagerecord':
            att = ATTSubscription.objects.get(pk=i['fields']['subscription'])
            usage_date = make_aware(datetime.strptime(i['fields']['usage_date'], "%Y-%m-%dT%H:%M:%S.%fZ"))
            obj = DataUsageRecord(att_subscription_id=att, price=float(i['fields']['price']),
                                  kilobytes_used=i['fields']['kilobytes_used'], usage_date=usage_date)
            data_objects.append(obj)
        else:
            att = ATTSubscription.objects.get(pk=i['fields']['subscription'])
            usage_date = make_aware(datetime.strptime(i['fields']['usage_date'], "%Y-%m-%dT%H:%M:%S.%fZ"))
            obj = VoiceUsageRecord(att_subscription_id=att, price=float(i['fields']['price']),
                                  seconds_used=i['fields']['seconds_used'], usage_date=usage_date)
            voice_objects.append(obj)
    DataUsageRecord.objects.bulk_create(data_objects)
    VoiceUsageRecord.objects.bulk_create(voice_objects)


if __name__ == '__main__':
    read_file('fixtures.json')
