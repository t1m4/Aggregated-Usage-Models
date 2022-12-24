from django.urls import path

from wingtel.usage import views

urlpatterns = [
    path("test/", views.TestView.as_view(), name="test"),
    path("price_limit/", views.UsageRecordPriceLimitView.as_view(), name="usage-price_limit"),
    path("usage_metrics/<int:subscription_id>/", views.UsageRecordTotalMetricsView.as_view(), name="usage-metrics"),
]
