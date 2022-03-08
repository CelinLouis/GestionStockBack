from rest_framework.fields import empty
from stock_bd.models.historique import Historique
from stock_bd.serializers.historique import HistoriqueSerializer
from stock_bd.pagination import PaginationPageNumberPagination
from rest_framework.decorators import APIView
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from stock_bd.serializers.stock import ProduitSerializer,ProduitCrudSerializer,ProduitModifieSerializer,ProduitEntrerSerializer,ProduitSortieSerializer
from rest_framework import status
from stock_bd.models.stock import Produit
from rest_framework.filters import SearchFilter, OrderingFilter


class ProduiteListe(ListAPIView):
    serializer_class = ProduitSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom_produit']
    pagination_class = PaginationPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Produit.objects.all().order_by('-date_ajoute')
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(nom_cproduit__icontains=query)
            ).distinct()
        return queryset_list


    def get_object(self, id):
        try:
            return Produit.objects.get(id=id)

        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self, request, *args, **kwargs):
        data = request.data
        if int(data['quantite_stock']) >= 0 and int(data['alerte_quantite']) >= 0:
            serializer = ProduitCrudSerializer(data=data)
            if serializer.is_valid():
                produite_exsistes = Produit.objects.filter(nom_produit = data.get('nom_produit')).count()
                if produite_exsistes == 0:
                    serializer.save()
                    idProd = serializer.data
                    id = idProd['id']
                    produit = self.get_object(id)
                    Historique.objects.create(produit=produit,quantite_stock=data['quantite_stock'],quantite_entrer=None,quantite_sortie=None,sortie_par=None)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({'message': 'produit existe deja'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'le quantite stock et alerte ne doit pas inferieur à 0'}, status=status.HTTP_400_BAD_REQUEST)

    
class ProduitAlerte(APIView):

    def get(self, request):
        data = request.data
        alertes = Produit.objects.filter(int(data['quantite_stock']) <= int(data['alerte_quantite']))
        serializer = ProduitSerializer(alertes, many=True)
        return Response(serializer.data)



class ProduitDetail(APIView):

    def get_object(self, id):
        try:
            return Produit.objects.get(id=id)

        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        produits = self.get_object(id)
        serializer = ProduitSerializer(produits)
        return Response(serializer.data)


    def get_produit_name(self, name):
        try:
            return Produit.objects.get(nom_produit=name)

        except Produit.DoesNotExist:
            return 0


    def put(self, request, id):
        produit = self.get_object(id)
        data=request.data
        serializer = ProduitModifieSerializer(produit, data=data)
        if serializer.is_valid():
            produit_existe = self.get_produit_name(data['nom_produit'])
            if produit_existe == 0:
                serializer.save()
                return Response(serializer.data)
            else:
                this_produit = ProduitModifieSerializer(produit).data 
                produit_existe = ProduitModifieSerializer(produit_existe).data
                if this_produit['id'] == produit_existe['id']:
                    serializer.save()
                    return Response(serializer.data)
                return Response({'message': 'Produit exciste deja'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        produit = self.get_object(id)
        produit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProduitEntrer(APIView):

    def get_object(self, id):
        try:
            return Produit.objects.get(id=id)

        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        produits = self.get_object(id)
        serializer = ProduitSerializer(produits)
        return Response(serializer.data)


    def put(self, request, id):
        produit = self.get_object(id)
        data=request.data
        if int(data['quantite_entrer']) <= 0:
            return Response({'message': 'le nombre que vous aviez entrer doit être sup à 0'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            quantite_stock = Produit.objects.get(id=produit.id).quantite_stock
            data['quantite_stock'] = quantite_stock + int(data['quantite_entrer'])
            serializer = ProduitEntrerSerializer(produit, data=data)
            if serializer.is_valid():
                serializer.save()
                quantite_stock = Produit.objects.get(id=produit.id).quantite_stock
                Historique.objects.create(produit=produit,quantite_stock=quantite_stock,quantite_entrer=data['quantite_entrer'],quantite_sortie=None,sortie_par=None)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProduitSortie(APIView):

    def get_object(self, id):
        try:
            return Produit.objects.get(id=id)

        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        produits = self.get_object(id)
        serializer = ProduitSerializer(produits)
        return Response(serializer.data)


    def put(self, request, id):
        produit = self.get_object(id)
        data=request.data
        qt_stock = Produit.objects.get(id=produit.id).quantite_stock
        if data['sortie_par'] is None:
            return Response({'message': 'Toutes les champs formulaire doit être remplie !'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if int(data['quantite_sortie']) > 0: 
                if int(data['quantite_sortie']) <= qt_stock:
                    data['quantite_stock'] = qt_stock - int(data['quantite_sortie'])
                    serializer = ProduitSortieSerializer(produit, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        quantite_stock = Produit.objects.get(id=produit.id).quantite_stock
                        Historique.objects.create(produit=produit,quantite_stock=quantite_stock,quantite_sortie=data['quantite_sortie'],sortie_par=data['sortie_par'],quantite_entrer=None)
                        return Response(serializer.data)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'le nombre depasse le quantite en stock'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'le nombre doit être superieur à zero'}, status=status.HTTP_400_BAD_REQUEST)
       