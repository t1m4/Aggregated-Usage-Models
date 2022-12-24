from django.contrib import admin

# Register your models here.
from wingtel.usage.models import DataUsageRecord, UsageRecord, VoiceUsageRecord


class AdminDataUsageRecord(admin.ModelAdmin):
    list_display = ["id", "subscription_id", "price", "usage_date", "kilobytes_used"]

    class Meta:
        model = DataUsageRecord


class AdminVoiceUsageRecord(admin.ModelAdmin):
    list_display = ["id", "subscription_id", "price", "usage_date", "seconds_used"]

    class Meta:
        model = VoiceUsageRecord


class AdminUsageRecord(admin.ModelAdmin):
    list_display = ["id", "type_of_usage", "subscription_id", "price", "usage_date", "used"]

    class Meta:
        model = VoiceUsageRecord


admin.site.register(DataUsageRecord, AdminDataUsageRecord)
admin.site.register(VoiceUsageRecord, AdminVoiceUsageRecord)
admin.site.register(UsageRecord, AdminUsageRecord)
