from rest_framework import serializers
from wingtel.purchases.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = '__all__'