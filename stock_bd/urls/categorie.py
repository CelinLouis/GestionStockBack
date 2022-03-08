from django.urls import path
from stock_bd.api.categorie import CategorieListe, CategorieDetails, CategorieSelect

urlpatterns = [
    path('categories/', CategorieListe.as_view()),
    path('categories/<int:id>/', CategorieDetails.as_view()),
    path('categoriesselect/', CategorieSelect.as_view())
]