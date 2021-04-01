from django.db.models import Count, Avg
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from wines.models import Country, Region, ProducerRegion, Producer, Grape, WineGrape, Wine, Vintage, GrapeAlias, Review

from . import custompermissions
from .serializers import CountrySerializer, RegionSerializer, ProducerRegionSerializer, ProducerSerializer, GrapeSerializer, WineGrapeSerializer, WineSerializer, VintageSerializer, \
    GrapeAliasSerializer, ReviewSerializer, VintageReviewSerializer, WineReviewSerializer, NewProducerSerializer, NewProducerRegionSerializer, NewGrapeSerializer, ProducerShortSerializer, \
    NewWineSerializer, NewWineGrapeSerializer, NewVintageSerializer, NewGrapeAliasSerializer, NewWineReviewSerializer, NewVintageReviewSerializer, RegionShortSerializer, WineShortSerializer, \
    GrapeShortSerializer, VintageShortSerializer

from django_filters import FilterSet, BooleanFilter, NumberFilter, ChoiceFilter, RangeFilter


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
    regions = Region.objects.filter(country=country)
    serializer = RegionShortSerializer(regions, many=True, context={'request': request})
    return Response(serializer.data)


class RegionList(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    name = 'region-list'

    filter_fields = (
        'country',
        'local_producers',
        'producers',
        'grapes',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
    )


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    name = 'region-detail'


""" ***BUGGED***
    
    Needs to be fixed!
    
    Requires adding an origin field to the Wine model, along with a check 
    constraint that ensures its origin matches one of the regions where the 
    its producer operates.  
"""
@api_view(['GET'])
def region_wines(request, pk):
    region = get_object_or_404(Region, pk=pk)
    wines = Wine.objects.filter(producer__origin=region)
    serializer = WineShortSerializer(wines, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def region_producers(request, pk):
    region = get_object_or_404(Region, pk=pk)
    producers = Producer.objects.filter(origin=region)
    serializer = ProducerShortSerializer(producers, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def region_grapes(request, pk):
    region = get_object_or_404(Region, pk=pk)
    grapes = Grape.objects.filter(origin=region)
    serializer = GrapeShortSerializer(grapes, many=True, context={'request': request})
    return Response(serializer.data)


class ProducerRegionList(generics.ListCreateAPIView):
    queryset = ProducerRegion.objects.all()
    name = 'producerregion-list'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewProducerRegionSerializer
        return ProducerRegionSerializer


class ProducerRegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProducerRegion.objects.all()
    name = 'producerregion-detail'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return NewProducerRegionSerializer
        return ProducerRegionSerializer


class ProducerList(generics.ListCreateAPIView):
    queryset = Producer.objects.all()
    name = 'producer-list'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewProducerSerializer
        return ProducerSerializer

    filter_fields = (
        'regions',
        'origin',
    )

    search_fields = (
        '^name',
    )

    ordering_fields = (
        'name',
        'regions',
    )


class ProducerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producer.objects.all()
    name = 'producer-detail'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return NewProducerSerializer
        return ProducerSerializer


@api_view(['GET'])
def producer_wines(request, pk):
    producer = get_object_or_404(Producer, pk=pk)
    wines = Wine.objects.filter(producer=producer)
    serializer = WineShortSerializer(wines, many=True, context={'request': request})
    return Response(serializer.data)


class GrapeList(generics.ListCreateAPIView):
    queryset = Grape.objects.all()
    name = 'grape-list'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewGrapeSerializer
        return GrapeSerializer

    filter_fields = (
        'origin',
        'type',
        # 'color',
        'body',
        'acidity',
    )

    search_fields = (
        '^name',
    )

    ordering_fields = (
        'name',
        'type',
        'body',
        'acidity',
    )


class GrapeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grape.objects.all()
    name = 'grape-detail'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return NewGrapeSerializer
        return GrapeSerializer


@api_view(['GET'])
def grape_wines(request, pk):
    grape = get_object_or_404(Grape, pk=pk)
    wines = Wine.objects.filter(grape_varieties=grape)
    serializer = WineShortSerializer(wines, many=True, context={'request': request})
    return Response(serializer.data)


class WineGrapeList(generics.ListCreateAPIView):
    queryset = WineGrape.objects.all()
    name = 'winegrape-list'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewWineGrapeSerializer
        return WineGrapeSerializer

    filter_fields = (
        'wine',
        'grape',
    )

    ordering_fields = (
        'wine',
        'grape',
    )


class WineGrapeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WineGrape.objects.all()
    name = 'winegrape-detail'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return NewWineGrapeSerializer
        return WineGrapeSerializer


class WineFilter(FilterSet):
    with_reviews = NumberFilter(field_name='reviews',
                                method='filter_with_reviews',
                                label='')
    min_average_score = NumberFilter(field_name='reviews__score',
                                     method='filter_min_average_score',
                                     label='Minimum average score')
    max_average_score = NumberFilter(field_name='reviews__score',
                                     method='filter_max_average_score',
                                     label='Maximum average score')


    def filter_with_reviews(self, queryset, name, value):
        return Wine.objects.annotate(review_count=Count('reviews')).filter(review_count__gte=value)

    def filter_min_average_score(self, queryset, name, value):
        return Wine.objects.annotate(review_count=Avg('reviews__score')).filter(review_count__gte=value)

    def filter_max_average_score(self, queryset, name, value):
        return Wine.objects.annotate(review_count=Avg('reviews__score')).filter(review_count__lte=value)

    class Meta:
        model = Wine
        fields = (
            'with_reviews',
            'min_average_score',
            'max_average_score',
        )


class WineList(generics.ListCreateAPIView):
    queryset = Wine.objects.all()
    name = 'wine-list'
    filter_class = WineFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewWineSerializer
        return WineSerializer
    filter_fields = (
        'type',
        'producer',
        'grape_varieties',
        'origin',
    )

    search_fields = (
        '^name',
        '^type',
    )

    ordering_fields = (
        'name',
        'type',
        'producer',
        'grape_varieties',
        'origin',
    )


class WineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    name = 'wine-detail'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return NewWineSerializer
        return WineSerializer




@api_view(['GET'])
def wine_vintages(request, pk):
    wine = get_object_or_404(Wine, pk=pk)
    vintages = Vintage.objects.filter(wine=wine)
    serializer = VintageShortSerializer(vintages, many=True, context={'request': request})
    return Response(serializer.data)


# @api_view(['GET'])
# def wine_reviews(request, pk):
#     wine = get_object_or_404(Wine, pk=pk)
#     reviews = Review.objects.filter(wine=wine)
#     serializer = ReviewSerializer(reviews, many=True, context={'request': request})
#     return Response(serializer.data)


class VintageList(generics.ListCreateAPIView):
    queryset = Vintage.objects.all()
    name = 'vintage-list'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewVintageSerializer
        return VintageSerializer
    filter_fields = (
        'wine',
        'year',
        'alcohol_content',
    )

    search_fields = (
        '^name',
    )

    ordering_fields = (
        'name',
        'year',
        'alcohol_content',
    )


class VintageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vintage.objects.all()
    name = 'vintage-detail'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return NewVintageSerializer
        return VintageSerializer


# @api_view(['GET'])
# def vintage_reviews(request, pk):
#     vintage = get_object_or_404(Vintage, pk=pk)
#     reviews = Review.objects.filter(vintage=vintage)
#     serializer = ReviewSerializer(reviews, many=True, context={'request': request})
#     return Response(serializer.data)


class GrapeAliasList(generics.ListCreateAPIView):
    queryset = GrapeAlias.objects.all()
    name = 'grapealias-list'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewGrapeAliasSerializer
        return GrapeAliasSerializer

    filter_fields = (
        'grape',
    )

    search_fields = (
        '^name',
    )

    ordering_fields = (
        'name',
    )


class GrapeAliasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GrapeAlias.objects.all()
    name = 'grapealias-detail'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return NewGrapeAliasSerializer
        return GrapeAliasSerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    name = 'review-list'

    def perform_create(self, serializer_class):
        serializer_class.save(user=self.request.user)

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    filter_fields = (
        'user',
        'wine',
        'vintage',
        'active',
    )

    search_fields = (
        'text',
    )

    ordering_fields = (
        'score',
    )


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    name = 'review-detail'

    def perform_create(self, serializer_class):
        serializer_class.save(user=self.request.user)

    def perform_update(self, serializer_class):
        instance = serializer_class.save()
        if self.request.user != instance.user and self.request.user.is_staff:
            serializer_class.save(text=f'(ADMIN EDIT BY {self.request.user}) ' + instance.text)

    permission_classes = (
        custompermissions.IsCurrentUserAdminOrOwnerOrReadOnly,
    )


class WineReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    name = 'wine-review-list'

    def perform_create(self, serializer_class):
        serializer_class.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewWineReviewSerializer
        return WineReviewSerializer


# class WineReviewDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     name = 'wine-review-detail'
#
#     def get_serializer_class(self):
#         if self.request.method == 'PUT':
#             return NewWineReviewSerializer
#         return WineReviewSerializer


class VintageReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    name = 'vintage-review-list'

    def perform_create(self, serializer_class):
        serializer_class.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewVintageReviewSerializer
        return VintageReviewSerializer


# class VintageReviewDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = VintageReviewSerializer
#     name = 'vintage-review-detail'
#
#     def get_serializer_class(self):
#         if self.request.method == 'PUT':
#             return NewVintageReviewSerializer
#         return VintageReviewSerializer


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'countries': reverse(CountryList.name, request=request),
            'regions': reverse(RegionList.name, request=request),
            'producers': reverse(ProducerList.name, request=request),
            'grapes': reverse(GrapeList.name, request=request),
            'wines': reverse(WineList.name, request=request),
            'vintages': reverse(VintageList.name, request=request),
            'grape-aliases': reverse(GrapeAliasList.name, request=request),
            'reviews': reverse(ReviewList.name, request=request),
            })

