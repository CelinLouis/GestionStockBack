from django.db.models.aggregates import Sum
from stock_bd.serializers.categorie import CategorieSerializer
from stock_bd.models.categorie import Categorie
from stock_bd.models.historique import Historique
from stock_bd.models.stock import Produit
from rest_framework import serializers 

class ProduitSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Produit
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ProduitSerializer, self).to_representation(instance)
        categorie = Categorie.objects.get(id=data['categorie'])
        data["categorie"] = CategorieSerializer(categorie).data
        total_sortie = 0
        sortie = Historique.objects.filter(produit=data['id']).values('produit').aggregate(sortie_total=Sum('quantite_sortie'))
        if sortie is not None:
            total_sortie = sortie["sortie_total"] or 0
        total_entrer = 0
        entrer = Historique.objects.filter(produit=data['id']).values('produit').aggregate(entrer_total=Sum('quantite_entrer'))
        if entrer is not None:
            total_entrer = entrer["entrer_total"] or 0
        data["total_sortie"]=total_sortie
        data["total_entrer"]=total_entrer
        return data


class ProduitCrudSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Produit
        fields = ('id','nom_produit','categorie','quantite_stock','alerte_quantite','date_ajoute')


class ProduitModifieSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Produit
        fields = ('id','nom_produit','categorie','alerte_quantite')
        
    def to_representation(self, instance):
        data = super(ProduitModifieSerializer, self).to_representation(instance)
        categorie = Categorie.objects.get(id=data['categorie'])
        data["categorie"] = CategorieSerializer(categorie).data
        return data


class ProduitEntrerSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Produit
        fields = ('id','quantite_stock')


class ProduitSortieSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Produit
        fields = ('id','quantite_stock')