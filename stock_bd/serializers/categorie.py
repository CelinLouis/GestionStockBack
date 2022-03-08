from stock_bd.models.categorie import Categorie
from rest_framework import serializers 


class CategorieSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Categorie
        fields = '__all__'