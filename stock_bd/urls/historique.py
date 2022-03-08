from django.urls import path
from stock_bd.api.historique import HistoriqueListe

urlpatterns = [
    path('historiques/', HistoriqueListe.as_view())
]