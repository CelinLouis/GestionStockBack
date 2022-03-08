from django.contrib import admin
from stock_bd.models.categorie import Categorie
from stock_bd.models.stock import Produit
from stock_bd.models.historique import Historique
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Historique)
TokenAdmin.raw_id_fields = ['user']