from stock_bd.models.stock import Produit
from django.db import models

class Historique(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite_stock = models.IntegerField(default='0', blank=True, null=True)
    quantite_entrer = models.IntegerField(default='0', blank=True, null=True)
    quantite_sortie = models.IntegerField(default='0', blank=True, null=True)
    sortie_par = models.CharField(max_length=50,blank=True, null=True)
    date_ajoute = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.produit.nom_produit + ' ' + str(self.produit.categorie.nom_categorie)+ ' ' + str(self.date_ajoute)