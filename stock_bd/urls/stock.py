from django.urls import path
from stock_bd.api.stock import ProduiteListe, ProduitDetail, ProduitEntrer, ProduitSortie, ProduitAlerte

urlpatterns = [
    path('produites/', ProduiteListe.as_view()),
    path('produites/<int:id>/', ProduitDetail.as_view()),
    path('entrer/<int:id>/', ProduitEntrer.as_view()),
    path('sortie/<int:id>/', ProduitSortie.as_view()),
    path('alertes/', ProduitAlerte.as_view())
]