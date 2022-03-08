from stock_bd.pagination import PaginationPageNumberPagination
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from stock_bd.serializers.historique import HistoriqueSerializer
from rest_framework import status
from stock_bd.models.historique import Historique
from rest_framework.filters import SearchFilter, OrderingFilter


class HistoriqueListe(ListAPIView):
    serializer_class = HistoriqueSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['produit']
    pagination_class = PaginationPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Historique.objects.all().order_by('-date_ajoute')
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(nom_cproduit__icontains=query)
            ).distinct()
        return queryset_list


    def post(self, request):
        data = request.data
        serializer = HistoriqueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request):
        historiques = Historique.objects.all()
        historiques.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)