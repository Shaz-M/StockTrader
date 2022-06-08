from django.urls import path
from . import views;
from stocks import views as tickerView

app_name = 'portfolio'
urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('positions/',views.positions,name='positions'),
    path('stocks/<str:tid>',tickerView.ticker,name='ticker'),
    path('search',views.navsearch,name='search')
]