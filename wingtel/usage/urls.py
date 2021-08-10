from django.urls import path

from wingtel.usage import views

urlpatterns = [
    path('fill/', views.FillModel.as_view(), name='usage-fill'),
    path('aggregate/', views.AggregateDataView.as_view(), name='usage-aggregate'),
    path('price_limit/', views.SubcsriptionExceededPrice.as_view(), name='usage-aggregate'),
    path('usage_metrics/<int:id>/', views.UsageMetrics.as_view(), name='usage-aggregate'),
]