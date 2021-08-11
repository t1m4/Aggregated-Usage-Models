from django.urls import path

from wingtel.usage import views

urlpatterns = [
    path('price_limit/', views.SubscriptionExceededPrice.as_view(), name='usage-price_limit'),
    path('usage_metrics/<int:id>/', views.UsageMetricsGenericsView.as_view(), name='usage-metrics'),
]