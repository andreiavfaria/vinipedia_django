from django.db.models import Count, Avg, Q
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle

from wines.models import Country, Region, ProducerRegion, Producer, Grape, WineGrape, Wine, Vintage, GrapeAlias, Review

from . import custompermissions
from .serializers import CountrySerializer, RegionSerializer, ProducerRegionSerializer, ProducerSerializer, GrapeSerializer, WineGrapeSerializer, WineSerializer, VintageSerializer, \
    GrapeAliasSerializer, ReviewSerializer, VintageReviewSerializer, WineReviewSerializer, NewProducerSerializer, NewProducerRegionSerializer, NewGrapeSerializer, ProducerShortSerializer, \
    NewWineSerializer, NewWineGrapeSerializer, NewVintageSerializer, NewGrapeAliasSerializer, NewWineReviewSerializer, NewVintageReviewSerializer, RegionShortSerializer, WineShortSerializer, \
    GrapeShortSerializer, VintageShortSerializer, VintageWithWineShortSerializer

from django_filters import FilterSet, BooleanFilter, NumberFilter, ChoiceFilter, RangeFilter, AllValuesFilter, MultipleChoiceFilter, ModelMultipleChoiceFilter, ModelChoiceFilter

from wines.utils import get_slice_min_max


class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    name = 'country-list'

    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
    )


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


@api_view(['GET'])
def country_producers(request, pk):
    country = get_object_or_404(Country, pk=pk)
    regions = Region.objects.filter(country=country)
    producers = Producer.objects.filter(origin__in=regions)
    serializer = ProducerShortSerializer(producers, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def country_wines(request, pk):
    country = get_object_or_404(Country, pk=pk)
    regions = Region.objects.filter(country=country)
    wines = Wine.objects.filter(origin__in=regions)
    serializer = WineShortSerializer(wines, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def country_grapes(request, pk):
    country = get_object_or_404(Country, pk=pk)
    regions = Region.objects.filter(country=country)
    grapes = Grape.objects.filter(origin__in=regions)
    serializer = GrapeShortSerializer(grapes, many=True, context={'request': request})
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

    throttle_scope = 'region'
    throttle_classes = (ScopedRateThrottle,)


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    name = 'region-detail'

    throttle_scope = 'region'
    throttle_classes = (ScopedRateThrottle,)


@api_view(['GET'])
def region_wines(request, pk):
    region = get_object_or_404(Region, pk=pk)
    wines = Wine.objects.filter(origin=region)
    serializer = WineShortSerializer(wines, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def region_producers(request, pk):
    region = get_object_or_404(Region, pk=pk)
    # hack using distinct() to remove duplicates, since the following query is
    # returning duplicate entries somehow:
    # Producer.objects.filter(Q(origin=region) | Q(presence=region))
    producers = Producer.objects.filter(Q(origin=region) | Q(presence=region)).distinct()
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
        'origin',
        'presence',
    )

    search_fields = (
        '^name',
    )

    ordering_fields = (
        'name',
    )

    throttle_scope = 'producer'
    throttle_classes = (ScopedRateThrottle,)


class ProducerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producer.objects.all()
    name = 'producer-detail'

    throttle_scope = 'producer'
    throttle_classes = (ScopedRateThrottle,)

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


@api_view(['GET'])
def producer_vintages(request, pk):
    producer = get_object_or_404(Producer, pk=pk)
    vintages = Vintage.objects.filter(wine__producer=producer)
    serializer = VintageWithWineShortSerializer(vintages, many=True, context={'request': request})
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
        # 'colour',
        'acidity',
        'body',
    )

    search_fields = (
        '^name',
    )

    ordering_fields = (
        'name',
        'type',
        'acidity',
        'body',
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
    type = MultipleChoiceFilter(choices=Wine.WINE_TYPE_CHOICES,
                             label='Wine type')
    producer = ModelMultipleChoiceFilter(queryset=Producer.objects.all(),
                                         field_name='producer__name',
                                         to_field_name='name',
                                         label='Producer')
    grape = ModelMultipleChoiceFilter(queryset=Grape.objects.all(),
                                      field_name='grapes__grape__name',
                                      to_field_name='name',
                                      label='Grape varieties')
    origin = ModelMultipleChoiceFilter(queryset=Region.objects.all(),
                                       field_name='origin__name',
                                       to_field_name='name',
                                       label='Origin')
    with_reviews = BooleanFilter(field_name='reviews',
                                 method='filter_with_reviews',
                                 label='WIth reviews only')
    nr_reviews = RangeFilter(method='filter_nr_reviews',
                             label='Number of reviews')
    nr_vintages = RangeFilter(method='filter_nr_vintages',
                              label='Number of vintages')
    nr_grape_varieties = RangeFilter(method='filter_nr_grape_varieties',
                                     label='Number of grape varieties')
    average_score = RangeFilter(method='filter_average_score',
                                label='Average score')
    average_acidity = RangeFilter(method='filter_average_acidity',
                                  label='Average acidity')
    average_body = RangeFilter(method='filter_average_body',
                               label='Average body')
    average_sweetness = RangeFilter(method='filter_average_sweetness',
                                    label='Average sweetness')
    average_tannin = RangeFilter(method='filter_average_tannin',
                                 label='Average tannin')

    def filter_with_reviews(self, queryset, name, value):
        if value:
            return queryset.annotate(review_count=Count('reviews')).filter(review_count__gte=1)
        else:
            return queryset.annotate(review_count=Count('reviews')).filter(review_count=0)

    def filter_average_score(self, queryset, name, value):
        # The value parameter that is passed by RangeFilter is a slice object
        # https://stackoverflow.com/a/36459896
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_score=Avg('reviews__score')).filter(avg_score__lte=max)
        elif max is None:
            return queryset.annotate(avg_score=Avg('reviews__score')).filter(avg_score__gte=min)
        else:
            return queryset.annotate(avg_score=Avg('reviews__score')).filter(avg_score__range=(min, max))

    def filter_nr_reviews(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(nr_reviews=Count('reviews')).filter(nr_reviews__lte=max)
        elif max is None:
            return queryset.annotate(nr_reviews=Count('reviews')).filter(nr_reviews__gte=min)
        else:
            return queryset.annotate(nr_reviews=Count('reviews')).filter(nr_reviews__range=(min, max))

    def filter_nr_vintages(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(nr_vintages=Count('vintages')).filter(nr_vintages__lte=max)
        elif max is None:
            return queryset.annotate(nr_vintages=Count('vintages')).filter(nr_vintages__gte=min)
        else:
            return queryset.annotate(nr_vintages=Count('vintages')).filter(nr_vintages__range=(min, max))

    def filter_nr_grape_varieties(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(nr_grapes=Count('grapes')).filter(nr_grapes__lte=max)
        elif max is None:
            return queryset.annotate(nr_grapes=Count('grapes')).filter(nr_grapes__gte=min)
        else:
            return queryset.annotate(nr_grapes=Count('grapes')).filter(nr_grapes__range=(min, max))

    def filter_average_acidity(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_acidity=Avg('reviews__acidity')).filter(avg_acidity__lte=max)
        elif max is None:
            return queryset.annotate(avg_acidity=Avg('reviews__acidity')).filter(avg_acidity__gte=min)
        else:
            return queryset.annotate(avg_acidity=Avg('reviews__acidity')).filter(avg_acidity__range=(min, max))

    def filter_average_body(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_body=Avg('reviews__body')).filter(avg_body__lte=max)
        elif max is None:
            return queryset.annotate(avg_body=Avg('reviews__body')).filter(avg_body__gte=min)
        else:
            return queryset.annotate(avg_body=Avg('reviews__body')).filter(avg_body__range=(min, max))

    def filter_average_sweetness(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_sweetness=Avg('reviews__sweetness')).filter(avg_sweetness__lte=max)
        elif max is None:
            return queryset.annotate(avg_sweetness=Avg('reviews__sweetness')).filter(avg_sweetness__gte=min)
        else:
            return queryset.annotate(avg_sweetness=Avg('reviews__sweetness')).filter(avg_sweetness__range=(min, max))

    def filter_average_tannin(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_tannin=Avg('reviews__tannin')).filter(avg_tannin__lte=max)
        elif max is None:
            return queryset.annotate(avg_tannin=Avg('reviews__tannin')).filter(avg_tannin__gte=min)
        else:
            return queryset.annotate(avg_tannin=Avg('reviews__tannin')).filter(avg_tannin__range=(min, max))

    class Meta:
        model = Wine
        fields = (
            'type',
            'producer',
            'grape',
            'origin',
            'with_reviews',
            'average_score',
        )


class WineList(generics.ListCreateAPIView):
    queryset = Wine.objects.all()
    name = 'wine-list'
    filter_class = WineFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewWineSerializer
        return WineSerializer

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

    throttle_scope = 'wine'
    throttle_classes = (ScopedRateThrottle,)


class WineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    name = 'wine-detail'

    throttle_scope = 'wine'
    throttle_classes = (ScopedRateThrottle,)

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


class VintageFilter(FilterSet):
    type = MultipleChoiceFilter(field_name='wine__type',
                        choices=Wine.WINE_TYPE_CHOICES,
                             label='Wine type')
    producer = ModelMultipleChoiceFilter(queryset=Producer.objects.all(),
                                         field_name='wine__producer__name',
                                         to_field_name='name',
                                         label='Producer')
    grape = ModelMultipleChoiceFilter(queryset=Grape.objects.all(),
                                      field_name='wine__grapes__grape__name',
                                      to_field_name='name',
                                      label='Grape varieties')
    origin = ModelMultipleChoiceFilter(queryset=Region.objects.all(),
                                       field_name='wine__origin__name',
                                       to_field_name='name',
                                       label='Origin')
    alcohol_content = RangeFilter(method='filter_alcohol_content',
                                  label='Alcohol content')
    with_reviews = BooleanFilter(field_name='reviews',
                                method='filter_with_reviews',
                                label='WIth reviews only')
    nr_reviews = RangeFilter(method='filter_nr_reviews',
                             label='Number of reviews')
    average_score = RangeFilter(method='filter_average_score',
                                label='Average score')
    nr_grape_varieties = RangeFilter(method='filter_nr_grape_varieties',
                                     label='Number of grape varieties')
    average_acidity = RangeFilter(method='filter_average_acidity',
                                  label='Average acidity')
    average_body = RangeFilter(method='filter_average_body',
                               label='Average body')
    average_sweetness = RangeFilter(method='filter_average_sweetness',
                                    label='Average sweetness')
    average_tannin = RangeFilter(method='filter_average_tannin',
                                 label='Average tannin')

    def filter_alcohol_content(self, queryset, name, value):
        print("filter_alcohol_content", queryset)
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.filter(alcohol_content__lte=max)
        elif max is None:
            return queryset.filter(alcohol_content__gte=min)
        else:
            return queryset.filter(alcohol_content__range=(min, max))

    def filter_with_reviews(self, queryset, name, value):
        print("filter_with_reviews", queryset)
        if value:
            return queryset.annotate(review_count=Count('reviews')).filter(review_count__gte=1)
        else:
            return queryset.annotate(review_count=Count('reviews')).filter(review_count=0)

    def filter_average_score(self, queryset, name, value):
        # The value parameter that is passed by RangeFilter is a slice object
        # https://stackoverflow.com/a/36459896
        print("filter_average_score", queryset)
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_score=Avg('reviews__score')).filter(avg_score__lte=max)
        elif max is None:
            return queryset.annotate(avg_score=Avg('reviews__score')).filter(avg_score__gte=min)
        else:
            return queryset.annotate(avg_score=Avg('reviews__score')).filter(avg_score__range=(min, max))

    def filter_nr_reviews(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(nr_reviews=Count('reviews')).filter(nr_reviews__lte=max)
        elif max is None:
            return queryset.annotate(nr_reviews=Count('reviews')).filter(nr_reviews__gte=min)
        else:
            return queryset.annotate(nr_reviews=Count('reviews')).filter(nr_reviews__range=(min, max))

    def filter_nr_grape_varieties(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(nr_grapes=Count('wine__grapes')).filter(nr_grapes__lte=max)
        elif max is None:
            return queryset.annotate(nr_grapes=Count('wine__grapes')).filter(nr_grapes__gte=min)
        else:
            return queryset.annotate(nr_grapes=Count('wine__grapes')).filter(nr_grapes__range=(min, max))

    def filter_average_acidity(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_acidity=Avg('reviews__acidity')).filter(avg_acidity__lte=max)
        elif max is None:
            return queryset.annotate(avg_acidity=Avg('reviews__acidity')).filter(avg_acidity__gte=min)
        else:
            return queryset.annotate(avg_acidity=Avg('reviews__acidity')).filter(avg_acidity__range=(min, max))

    def filter_average_body(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_body=Avg('reviews__body')).filter(avg_body__lte=max)
        elif max is None:
            return queryset.annotate(avg_body=Avg('reviews__body')).filter(avg_body__gte=min)
        else:
            return queryset.annotate(avg_body=Avg('reviews__body')).filter(avg_body__range=(min, max))

    def filter_average_sweetness(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_sweetness=Avg('reviews__sweetness')).filter(avg_sweetness__lte=max)
        elif max is None:
            return queryset.annotate(avg_sweetness=Avg('reviews__sweetness')).filter(avg_sweetness__gte=min)
        else:
            return queryset.annotate(avg_sweetness=Avg('reviews__sweetness')).filter(avg_sweetness__range=(min, max))

    def filter_average_tannin(self, queryset, name, value):
        min, max = get_slice_min_max(value)
        if min is None:
            return queryset.annotate(avg_tannin=Avg('reviews__tannin')).filter(avg_tannin__lte=max)
        elif max is None:
            return queryset.annotate(avg_tannin=Avg('reviews__tannin')).filter(avg_tannin__gte=min)
        else:
            return queryset.annotate(avg_tannin=Avg('reviews__tannin')).filter(avg_tannin__range=(min, max))

    class Meta:
        model = Vintage
        fields = (
            'year',
            'type',
            'producer',
            'grape',
            'origin',
            'with_reviews',
            'nr_reviews',
            'average_score',
        )


class VintageList(generics.ListCreateAPIView):
    queryset = Vintage.objects.all()
    name = 'vintage-list'
    filter_class = VintageFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewVintageSerializer
        return VintageSerializer

    search_fields = (
        'wine__name',
        'wine__type',
    )

    ordering_fields = (
        'wine__name',
        'wine__type',
        'year',
        'alcohol_content',
    )

    throttle_scope = 'vintage'
    throttle_classes = (ScopedRateThrottle,)


class VintageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vintage.objects.all()
    name = 'vintage-detail'

    throttle_scope = 'vintage'
    throttle_classes = (ScopedRateThrottle,)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return NewVintageSerializer
        return VintageSerializer


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
    serializer_class = ReviewSerializer
    name = 'review-list'

    def get_queryset(self):
        user = self.request.user
        print(user, user.is_staff)
        if not user.is_authenticated:
            return Review.objects.none()
        if user.is_staff:
            return Review.objects.all()
        else:
            return Review.objects.filter(user=user, active=True)

    def perform_create(self, serializer_class):
        serializer_class.save(user=self.request.user)

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    filter_fields = (
        'user',
        'wine',
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


@api_view(['GET'])
def wine_reviews(request, pk):
    wine = get_object_or_404(Wine, pk=pk)
    reviews = Review.objects.filter(wine=wine)
    serializer = WineReviewSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def vintage_reviews(request, pk):
    vintage = get_object_or_404(Vintage, pk=pk)
    reviews = Review.objects.filter(vintage=vintage)
    serializer = VintageReviewSerializer(reviews, many=True, context={'request': request})
    return Response(serializer.data)


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

