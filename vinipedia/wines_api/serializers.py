from rest_framework import serializers

from wines.models import Country, Region, Producer, Grape, ProducerRegion, Wine, WineGrape, Vintage, GrapeAlias, Review


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country
        fields = (
            'url',
            'pk',
            'name',
            # 'regions',
            # 'region_list'
        )


class RegionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Region
        fields = (
            'url',
            'pk',
            'name',
            'country',
            'description',
        )


class ProducerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Producer
        fields = (
            'url',
            'pk',
            'name',
            'origin',
            'presence',
            'description',
        )


class ProducerRegionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProducerRegion
        fields = (
            'url',
            'pk',
            'producer',
            'region',
        )


class GrapeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Grape
        fields = (
            'url',
            'pk',
            'name',
            'type',
            'description',
        )


class WineSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Wine
        fields = (
            'url',
            'pk',
            'name',
            'producer',
            'grape_varieties',
            'type',
            'description',
        )


class WineGrapeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WineGrape
        fields = (
            'url',
            'pk',
            'wine',
            'grape',
        )


class VintageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vintage
        fields = (
            'url',
            'pk',
            'wine',
            'year',
            'description',
        )


class GrapeAliasSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GrapeAlias
        fields = (
            'url',
            'pk',
            'name',
            'grape',
        )


class ReviewSerializer(serializers.HyperlinkedModelSerializer):

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
            'published_on',
            'updated',
            'active',
        )
