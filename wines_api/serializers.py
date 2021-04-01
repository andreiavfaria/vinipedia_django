from rest_framework import serializers

from wines.models import Country, Region, Producer, Grape, ProducerRegion, Wine, WineGrape, Vintage, GrapeAlias, Review


class RegionShortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Region
        fields = (
            'url',
            'name',
        )


class ProducerShortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Producer
        fields = (
            'url',
            'name',
        )


class GrapeShortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Grape
        fields = (
            'url',
            'name',
            'type',
        )


class WineShortSerializer(serializers.HyperlinkedModelSerializer):

    producer = ProducerShortSerializer()

    class Meta:
        model = Wine
        fields = (
            'url',
            'name',
            'type',
            'producer',
        )


class VintageShortSerializer(serializers.HyperlinkedModelSerializer):

    wine = WineShortSerializer()

    class Meta:
        model = Vintage
        fields = (
            'url',
            'wine',
            'year',
        )


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    region_list = serializers.HyperlinkedIdentityField(view_name='country-region-list', read_only=True)
    nr_regions = serializers.IntegerField(source='regions.count', read_only=True)
    regions = RegionShortSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = (
            'url',
            'pk',
            'name',
            'image',
            'nr_regions',
            'region_list',
            'regions',
        )


class RegionSerializer(serializers.HyperlinkedModelSerializer):

    wine_list = serializers.HyperlinkedIdentityField(view_name='region-wine-list', read_only=True)
    producer_list = serializers.HyperlinkedIdentityField(view_name='region-producer-list', read_only=True)
    grape_list = serializers.HyperlinkedIdentityField(view_name='region-grape-list', read_only=True)
    # bugged: see views.region_wines note!
    # nr_wines = serializers.IntegerField(source='wines.count')
    nr_producers = serializers.IntegerField(source='producers.count', read_only=True)
    nr_grapes = serializers.IntegerField(source='grapes.count', read_only=True)

    class Meta:
        model = Region
        fields = (
            'url',
            'pk',
            'name',
            'country',
            'image',
            'description',
            # 'nr_wines',
            'nr_producers',
            # 'nr_producers_from',
            # 'nr_producers_in_operation',
            'nr_grapes',
            'wine_list',
            'producer_list',
            'grape_list',
        )


class NewProducerSerializer(serializers.HyperlinkedModelSerializer):

    presence = serializers.SlugRelatedField(queryset=Region.objects.all(), many=True, slug_field='name')

    class Meta:
        model = Producer
        fields = (
            'url',
            'pk',
            'name',
            'short_name',
            'origin',
            'presence',
            'website',
            'email',
            'image',
            'description',
        )


class ProducerSerializer(NewProducerSerializer):

    origin = RegionShortSerializer()
    presence = RegionShortSerializer(many=True)
    wine_list = serializers.HyperlinkedIdentityField(view_name='producer-wine-list', read_only=True)
    nr_wines = serializers.IntegerField(source='wines.count', read_only=True)

    class Meta:
        model = Producer
        fields = (
            'url',
            'pk',
            'name',
            'short_name',
            'origin',
            'presence',
            'website',
            'email',
            'image',
            'description',
            'nr_wines',
            'wine_list',
        )


class NewProducerRegionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProducerRegion
        fields = (
            'url',
            'pk',
            'producer',
            'region',
        )


class ProducerRegionSerializer(NewProducerRegionSerializer):

    region = RegionShortSerializer()
    producer = ProducerShortSerializer()

    class Meta:
        model = ProducerRegion
        fields = (
            'url',
            'pk',
            'producer',
            'region',
        )


class NewGrapeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Grape
        fields = (
            'url',
            'pk',
            'name',
            'origin',
            'type',
            # 'colour',
            'body',
            'acidity',
            'image',
            'description',
        )


class GrapeSerializer(NewGrapeSerializer):

    origin = RegionShortSerializer()
    aliases = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    wine_list = serializers.HyperlinkedIdentityField(view_name='grape-wine-list', read_only=True)
    nr_wines = serializers.IntegerField(source='wines.count', read_only=True)

    class Meta:
        model = Grape
        fields = (
            'url',
            'pk',
            'name',
            'aliases',
            'origin',
            'type',
            # 'colour',
            'body',
            'acidity',
            'image',
            'description',
            'nr_wines',
            'wine_list',
        )


class NewWineSerializer(serializers.HyperlinkedModelSerializer):

    grape_varieties = serializers.SlugRelatedField(queryset=Grape.objects.all(), many=True, slug_field='name')

    class Meta:
        model = Wine
        fields = (
            'url',
            'pk',
            'name',
            'origin',
            'producer',
            'grape_varieties',
            'type',
            'image',
            'description',
        )


class WineSerializer(NewWineSerializer):

    producer = ProducerShortSerializer()
    grape_varieties = GrapeShortSerializer(many=True)
    vintage_list = serializers.HyperlinkedIdentityField(view_name='wine-vintage-list', read_only=True)
    review_list = serializers.HyperlinkedIdentityField(view_name='wine-review-list', read_only=True)
    nr_vintages = serializers.IntegerField(source='vintages.count', read_only=True)
    nr_reviews = serializers.IntegerField(source='reviews.count', read_only=True)
    average_score = serializers.FloatField(source='get_average_rating', read_only=True)

    class Meta:
        model = Wine
        fields = (
            'url',
            'pk',
            'name',
            'origin',
            'producer',
            'grape_varieties',
            'type',
            'image',
            'description',
            'nr_vintages',
            'nr_reviews',
            'average_score',
            'vintage_list',
            'review_list',
        )


class NewWineGrapeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WineGrape
        fields = (
            'url',
            'pk',
            'wine',
            'grape',
        )


class WineGrapeSerializer(NewWineGrapeSerializer):

    wine = WineShortSerializer()
    grape = GrapeShortSerializer()

    class Meta:
        model = WineGrape
        fields = (
            'url',
            'pk',
            'wine',
            'grape',
        )


class NewVintageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vintage
        fields = (
            'url',
            'pk',
            'wine',
            'year',
            'alcohol_content',
            'image',
            'description',
        )


class VintageSerializer(NewVintageSerializer):

    wine = WineShortSerializer()
    review_list = serializers.HyperlinkedIdentityField(view_name='vintage-review-list', read_only=True)
    nr_reviews = serializers.IntegerField(source='reviews.count', read_only=True)

    class Meta:
        model = Vintage
        fields = (
            'url',
            'pk',
            'wine',
            'year',
            'alcohol_content',
            'image',
            'description',
            'nr_reviews',
            'review_list',
        )


class NewGrapeAliasSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GrapeAlias
        fields = (
            'url',
            'pk',
            'name',
            'grape',
        )


class GrapeAliasSerializer(NewGrapeAliasSerializer):

    grape = GrapeShortSerializer()

    class Meta:
        model = GrapeAlias
        fields = (
            'url',
            'pk',
            'name',
            'grape',
        )


class ReviewSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = (
            'url',
            'pk',
            'wine',
            'vintage',
            'user',
            'text',
            'score',
            'sweetness',
            'body',
            'acidity',
            'tannin',
            'published_on',
            'updated',
        )


class NewWineReviewSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = (
            'url',
            'pk',
            'wine',
            'user',
            'text',
            'score',
            'sweetness',
            'body',
            'acidity',
            'tannin',
            'published_on',
            'updated',
        )


class WineReviewSerializer(NewWineReviewSerializer):

    wine = WineShortSerializer()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = (
            'url',
            'pk',
            'wine',
            'user',
            'text',
            'score',
            'sweetness',
            'body',
            'acidity',
            'tannin',
            'published_on',
            'updated',
        )


class NewVintageReviewSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = (
            'url',
            'pk',
            'vintage',
            'user',
            'text',
            'score',
            'sweetness',
            'body',
            'acidity',
            'tannin',
            'published_on',
            'updated',
        )


class VintageReviewSerializer(NewVintageReviewSerializer):

    vintage = VintageShortSerializer()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = (
            'url',
            'pk',
            'vintage',
            'user',
            'text',
            'score',
            'sweetness',
            'body',
            'acidity',
            'tannin',
            'published_on',
            'updated',
        )


