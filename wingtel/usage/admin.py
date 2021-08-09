from django.contrib import admin

# Register your models here.
from wingtel.usage.models import DataUsageRecord, VoiceUsageRecord

admin.site.register(DataUsageRecord)
admin.site.register(VoiceUsageRecord)