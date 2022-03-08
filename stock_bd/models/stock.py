from stock_bd.models.categorie import Categorie
from django.db import models

class Produit(models.Model):
    nom_produit = models.CharField(max_length=50, blank=False, null=False)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    quantite_stock = models.IntegerField(default='0', blank=True, null=True)
    alerte_quantite = models.IntegerField(default='0', blank=True, null=True)
    date_ajoute = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.nom_produit + ' ' + str(self.categorie.nom_categorie)+ ' ' + str(self.date_ajoute)