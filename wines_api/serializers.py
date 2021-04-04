from rest_framework import serializers

from wines.models import Country, Region, Producer, Grape, ProducerRegion, Wine, WineGrape, Vintage, GrapeAlias, Review


class RegionShortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Region
        fields = (
            'url',
            'name',
            'image',
        )


class ProducerShortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Producer
        fields = (
            'url',
            'name',
            'short_name',
            'image',
        )


class GrapeShortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Grape
        fields = (
            'url',
            'name',
            'type',
            'image',
        )


class WineShortSerializer(serializers.HyperlinkedModelSerializer):

    producer = ProducerShortSerializer()
    origin = RegionShortSerializer()

    class Meta:
        model = Wine
        fields = (
            'url',
            'name',
            'type',
            'producer',
            'origin',
            'image',
        )


class VintageShortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vintage
        fields = (
            'url',
            'year',
            'image',
        )


class VintageWithWineShortSerializer(serializers.HyperlinkedModelSerializer):

    wine = WineShortSerializer()

    class Meta:
        model = Vintage
        fields = (
            'url',
            'wine',
            'year',
            'image',
        )


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    nr_regions = serializers.IntegerField(source='regions.count', read_only=True)
    nr_producers = serializers.IntegerField(source='get_local_producers.count', read_only=True)
    nr_wines = serializers.IntegerField(source='get_local_wines.count', read_only=True)
    nr_grapes = serializers.IntegerField(source='get_local_grapes.count', read_only=True)
    region_list = serializers.HyperlinkedIdentityField(view_name='country-region-list', read_only=True)
    regions = RegionShortSerializer(many=True, read_only=True)
    producer_list = serializers.HyperlinkedIdentityField(view_name='country-producer-list', read_only=True)
    producers = ProducerShortSerializer(source='get_local_producers', many=True, read_only=True)
    wine_list = serializers.HyperlinkedIdentityField(view_name='country-wine-list', read_only=True)
    wines = WineShortSerializer(source='get_local_wines', many=True, read_only=True)
    grape_list = serializers.HyperlinkedIdentityField(view_name='country-grape-list', read_only=True)
    grapes = GrapeShortSerializer(source='get_local_grapes', many=True, read_only=True)
    average_wine_rating = serializers.FloatField(source='get_average_rating', read_only=True)

    class Meta:
        model = Country
        fields = (
            'url',
            'pk',
            'name',
            'image',
            'nr_regions',
            'nr_producers',
            'nr_wines',
            'nr_grapes',
            'average_wine_rating',
            'region_list',
            'regions',
            'producer_list',
            'producers',
            'wine_list',
            'wines',
            'grape_list',
            'grapes',
        )


class RegionSerializer(serializers.HyperlinkedModelSerializer):

    nr_producers = serializers.IntegerField(source='producers.count', read_only=True)
    # local_producers = serializers.IntegerField(source='local_producers.count', read_only=True)
    # other_producers = serializers.IntegerField(source='get_other_producers.count', read_only=True)
    nr_wines = serializers.IntegerField(source='local_wines.count')
    nr_grapes = serializers.IntegerField(source='grapes.count', read_only=True)
    producer_list = serializers.HyperlinkedIdentityField(view_name='region-producer-list', read_only=True)
    wine_list = serializers.HyperlinkedIdentityField(view_name='region-wine-list', read_only=True)
    grape_list = serializers.HyperlinkedIdentityField(view_name='region-grape-list', read_only=True)
    average_wine_rating = serializers.FloatField(source='get_average_rating', read_only=True)

    class Meta:
        model = Region
        fields = (
            'url',
            'pk',
            'name',
            'country',
            'image',
            'description',
            'nr_producers',
            # 'local_producers',
            # 'other_producers',
            'nr_wines',
            'nr_grapes',
            'average_wine_rating',
            'producer_list',
            'wine_list',
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
    nr_wines = serializers.IntegerField(source='wines.count', read_only=True)
    nr_vintages = serializers.IntegerField(source='get_producer_vintages.count', read_only=True)
    wine_list = serializers.HyperlinkedIdentityField(view_name='producer-wine-list', read_only=True)
    vintage_list = serializers.HyperlinkedIdentityField(view_name='producer-vintage-list', read_only=True)
    average_wine_rating = serializers.FloatField(source='get_producer_average_rating', read_only=True)

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
            'nr_vintages',
            'average_wine_rating',
            'wine_list',
            'vintage_list',
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
    nr_wines = serializers.IntegerField(source='wines.count', read_only=True)
    wine_list = serializers.HyperlinkedIdentityField(view_name='grape-wine-list', read_only=True)
    average_wine_rating = serializers.FloatField(source='get_average_rating', read_only=True)
    average_wine_acidity = serializers.FloatField(source='get_average_acidity', read_only=True)
    average_wine_body = serializers.FloatField(source='get_average_body', read_only=True)
    average_wine_sweetness = serializers.FloatField(source='get_average_sweetness', read_only=True)
    average_wine_tannin = serializers.FloatField(source='get_average_tannin', read_only=True)

    class Meta:
        model = Grape
        fields = (
            'url',
            'pk',
            'name',
            'aliases',
            'origin',
            'type',
            'acidity',
            'body',
            # 'colour',
            'image',
            'description',
            'nr_wines',
            'average_wine_rating',
            'average_wine_acidity',
            'average_wine_body',
            'average_wine_sweetness',
            'average_wine_tannin',
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

    origin = RegionShortSerializer()
    producer = ProducerShortSerializer()
    grape_varieties = GrapeShortSerializer(many=True)
    nr_vintages = serializers.IntegerField(source='vintages.count', read_only=True)
    nr_reviews = serializers.IntegerField(source='reviews.count', read_only=True)
    vintage_list = serializers.HyperlinkedIdentityField(view_name='wine-vintage-list', read_only=True)
    review_list = serializers.HyperlinkedIdentityField(view_name='wine-review-list', read_only=True)
    average_score = serializers.FloatField(source='get_average_rating', read_only=True)
    average_acidity = serializers.FloatField(source='get_average_acidity', read_only=True)
    average_body = serializers.FloatField(source='get_average_body', read_only=True)
    average_sweetness = serializers.FloatField(source='get_average_sweetness', read_only=True)
    average_tannin = serializers.FloatField(source='get_average_tannin', read_only=True)

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
            'average_acidity',
            'average_body',
            'average_sweetness',
            'average_tannin',
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
    average_score = serializers.FloatField(source='get_average_rating', read_only=True)
    average_acidity = serializers.FloatField(source='get_average_acidity', read_only=True)
    average_body = serializers.FloatField(source='get_average_body', read_only=True)
    average_sweetness = serializers.FloatField(source='get_average_sweetness', read_only=True)
    average_tannin = serializers.FloatField(source='get_average_tannin', read_only=True)

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
            'average_score',
            'average_acidity',
            'average_body',
            'average_sweetness',
            'average_tannin',
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
            'acidity',
            'body',
            'sweetness',
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
            'acidity',
            'body',
            'sweetness',
            'tannin',
            'published_on',
            'updated',
        )


class WineReviewSerializer(NewWineReviewSerializer):

    wine = WineShortSerializer()
    vintage = VintageShortSerializer()
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
            'acidity',
            'body',
            'sweetness',
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
            'acidity',
            'body',
            'sweetness',
            'tannin',
            'published_on',
            'updated',
        )


class VintageReviewSerializer(NewVintageReviewSerializer):

    vintage = VintageWithWineShortSerializer()
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
            'acidity',
            'body',
            'sweetness',
            'tannin',
            'published_on',
            'updated',
        )


