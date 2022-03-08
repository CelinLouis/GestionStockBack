from stock_bd.pagination import PaginationPageNumberPagination
from rest_framework.decorators import APIView
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from stock_bd.serializers.categorie import CategorieSerializer
from rest_framework import status
from stock_bd.models.categorie import Categorie
from rest_framework.filters import SearchFilter, OrderingFilter


class CategorieListe(ListAPIView):
    serializer_class = CategorieSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom_categorie']
    pagination_class = PaginationPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Categorie.objects.all().order_by('-date_ajoute')
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(nom_categorie__icontains=query)
            ).distinct()
        return queryset_list

    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CategorieSerializer(data=data)
        if serializer.is_valid():
            categorie_exsistes = Categorie.objects.filter(nom_categorie = data.get('nom_categorie')).count()
            if categorie_exsistes == 0:
                Categorie.objects.create(nom_categorie=data.get('nom_categorie'))
                return Response({'nom_categorie': data.get('nom_categorie')}, status=status.HTTP_201_CREATED)
            return Response({'message': 'categorie existe deja'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategorieSelect(APIView):

    def get(self, request):
        categories = Categorie.objects.all().order_by('-date_ajoute')
        serializer = CategorieSerializer(categories, many=True)
        return Response(serializer.data)


class CategorieDetails(APIView):

    def get_object(self, id):
        try:
            return Categorie.objects.get(id=id)

        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        categories = self.get_object(id)
        serializer = CategorieSerializer(categories)
        return Response(serializer.data)
    

    def get_categorie_name(self, name):
        try:
            return Categorie.objects.get(nom_categorie=name)

        except Categorie.DoesNotExist:
            return 0


    def put(self, request, id):
        categorie = self.get_object(id)
        data=request.data
        serializer = CategorieSerializer(categorie, data=data)
        if serializer.is_valid():
            categorie_existe = self.get_categorie_name(data['nom_categorie'])
            if categorie_existe == 0:
                serializer.save()
                return Response(serializer.data)
            else:
                this_categorie = CategorieSerializer(categorie).data 
                categorie_existe = CategorieSerializer(categorie_existe).data
                if this_categorie['id'] == categorie_existe['id']:
                    serializer.save()
                    return Response(serializer.data)
                return Response({'message': 'Categorie exciste deja'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        categorie = self.get_object(id)
        categorie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)