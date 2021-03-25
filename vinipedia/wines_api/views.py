from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from wines.models import Country, Region, ProducerRegion, Producer, Grape, WineGrape, Wine, Vintage, GrapeAlias, Review

from .serializers import CountrySerializer, RegionSerializer, ProducerRegionSerializer, ProducerSerializer, GrapeSerializer, WineGrapeSerializer, WineSerializer, VintageSerializer, \
    GrapeAliasSerializer, ReviewSerializer


class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    name = 'country-list'


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    name = 'country-detail'


@api_view(['GET'])
def country_regions(request, pk):
    country = get_object_or_404(Country, pk=pk)
    reviews = Review.objects.filter(country=country)
    serializer = ReviewSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data)


class RegionList(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    name = 'region-list'


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    name = 'region-detail'


@api_view(['GET'])
def region_wines(request, pk):
    pass


@api_view(['GET'])
def region_producers(request, pk):
    pass


@api_view(['GET'])
def region_grapes(request, pk):
    pass


class ProducerRegionList(generics.ListCreateAPIView):
    queryset = ProducerRegion.objects.all()
    serializer_class = ProducerRegionSerializer
    name = 'producerregion-list'


class ProducerRegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProducerRegion.objects.all()
    serializer_class = ProducerRegionSerializer
    name = 'producerregion-detail'


class ProducerList(generics.ListCreateAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    name = 'producer-list'


class ProducerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    name = 'producer-detail'


@api_view(['GET'])
def producer_wines(request, pk):
    pass


class GrapeList(generics.ListCreateAPIView):
    queryset = Grape.objects.all()
    serializer_class = GrapeSerializer
    name = 'grape-list'


class GrapeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grape.objects.all()
    serializer_class = GrapeSerializer
    name = 'grape-detail'


@api_view(['GET'])
def grape_wines(request, pk):
    pass


class WineGrapeList(generics.ListCreateAPIView):
    queryset = WineGrape.objects.all()
    serializer_class = WineGrapeSerializer
    name = 'winegrape-list'


class WineGrapeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WineGrape.objects.all()
    serializer_class = WineGrapeSerializer
    name = 'winegrape-detail'


class WineList(generics.ListCreateAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    name = 'wine-list'


@api_view(['GET'])
def wine_vintages(request, pk):
    pass


@api_view(['GET'])
def wine_reviews(request, pk):
    pass


class WineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    name = 'wine-detail'


class VintageList(generics.ListCreateAPIView):
    queryset = Vintage.objects.all()
    serializer_class = VintageSerializer
    name = 'vintage-list'


class VintageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vintage.objects.all()
    serializer_class = VintageSerializer
    name = 'vintage-detail'


@api_view(['GET'])
def vintage_reviews(request, pk):
    pass


class GrapeAliasList(generics.ListCreateAPIView):
    queryset = GrapeAlias.objects.all()
    serializer_class = GrapeAliasSerializer
    name = 'grapealias-list'


class GrapeAliasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GrapeAlias.objects.all()
    serializer_class = GrapeAliasSerializer
    name = 'grapealias-detail'


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    name = 'review-list'


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    name = 'review-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'countries': reverse(CountryList.name, request=request),
            'regions': reverse(RegionList.name, request=request),
            'producer-regions': reverse(ProducerRegionList.name, request=request),
            'producers': reverse(ProducerList.name, request=request),
            'grapes': reverse(GrapeList.name, request=request),
            'wine-grapes': reverse(WineGrapeList.name, request=request),
            'wines': reverse(WineList.name, request=request),
            'vintages': reverse(VintageList.name, request=request),
            'grape-aliases': reverse(GrapeAliasList.name, request=request),
            'reviews': reverse(ReviewList.name, request=request),
            })

