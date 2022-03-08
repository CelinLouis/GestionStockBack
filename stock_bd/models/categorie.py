from django.db import models

class Categorie(models.Model):
    nom_categorie = models.CharField(max_length=50)
    date_ajoute = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.nom_categorie + ' ' + str(self.date_ajoute)
