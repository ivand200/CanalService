from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from datetime import datetime
import gspread
import pandas as pd
import telegram_send
import xml.etree.ElementTree as ET
import requests
import logging

from .serializers import OrderSerializer
from .models import Order
from .creds import credentials
# Create your views here.

logger = logging.getLogger(__name__)


def get_usd(usd: float) -> float:
    """
    Get usd/rub exchange rate from cbr
    """
    r = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
    myroot = ET.fromstring(r.content)
    for i in myroot.findall("Valute"):
        item = i.find("CharCode").text
        price = i.find("Value").text
        if item == "USD":
            rub = float(price.replace(",","."))
            break
    rub_price = usd * rub
    return rub_price  # myroot[11][4]


class OrderList(APIView):
    """
    List of all orders
    """

    def get(self, request):
        orders = Order.objects.all()
        logger.info(f"Get list of {len(orders)} orders at {datetime.now()}")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class UpdateOrder(APIView):
    """
    Update orders from google sheet
    """

    def post(self, request):
        gc = gspread.service_account_from_dict(credentials)
        sh = gc.open("Orders")
        worksheet = sh.sheet1
        # dataframe = pd.DataFrame(worksheet.get_all_records())
        list_of_dicts = worksheet.get_all_records()
        records = [
            Order(
                id=record["№"],
                number=record["заказ №"],
                value=record["стоимость,$"],
                delivery_time=datetime.strptime(record["срок поставки"], "%d.%m.%Y"),
                value_at_rub=round(get_usd(record["стоимость,$"]), 2),
            )
            for record in list_of_dicts
        ]
        logger.info(f"Received {len(records)} orders at {datetime.now()}")
        Order.objects.bulk_create(records, ignore_conflicts=True)
        return JsonResponse({"status": "ok"}, status=200)

