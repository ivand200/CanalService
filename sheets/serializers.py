from rest_framework import serializers

from .models import Order


from datetime import datetime


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order parsing google sheet
    """

    class Meta:
        model = Order
        fields = "__all__"



# class OrderViewSerializer(serializers.Serializer):
#     """
#     """
#     id = serializers.IntegerField(source="№")
#     number = serializers.IntegerField(source="заказ №")
#     value = serializers.FloatField(source="стоимость,$")
#     delivery_time = serializers.DateField(source="срок поставки")
#     value_at_rub = serializers.SerializerMethodField()