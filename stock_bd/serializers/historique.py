from stock_bd.serializers.stock import ProduitSerializer
from stock_bd.models.stock import Produit
from stock_bd.models.historique import Historique
from rest_framework import serializers 

class HistoriqueSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Historique
        fields = '__all__'


    def to_representation(self, instance):
        data = super(HistoriqueSerializer, self).to_representation(instance)
        produit = Produit.objects.get(id=data['produit'])
        data["produit"] = ProduitSerializer(produit).data
        return data
