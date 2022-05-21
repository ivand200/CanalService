from django.urls import path
from sheets import views

urlpatterns = [
    path("sheet/", views.UpdateOrder.as_view()),
    path("orders/", views.OrderList.as_view()),
]