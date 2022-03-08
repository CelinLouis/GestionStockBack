from stock_bd.urls.stock import urlpatterns as StockUrls
from stock_bd.urls.categorie import urlpatterns as CategorieUrls
from stock_bd.urls.historique import urlpatterns as HistoriqueUrls

urlpatterns = CategorieUrls + StockUrls + HistoriqueUrls