from django.urls import path
from . import views;
from stocks import views as tickerView

urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('positions/',views.positions,name='positons'),
    path('stocks/<str:tid>',tickerView.ticker,name='ticker')
]