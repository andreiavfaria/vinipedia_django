from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.urls import reverse


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                related_name='regions')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (('name', 'country',),)
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wines:region_detail',
                       args=[self.id])


class Producer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    origin = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name='local_producers')
    presence = models.ManyToManyField(Region,
                                      through='ProducerRegion',
                                      through_fields=('producer', 'region'))
    description = models.TextField(blank=True)
    # ^^^^ country (derived from region)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wines:producer_detail',
                       args=[self.id])


class ProducerRegion(models.Model):
    """ Intermediary table for the regions where a producer operates.

        (Bacalhôa Vinhos de Portugal, for instance, operates in 7 different
        regions)

    """
    producer = models.ForeignKey(Producer,
                                 on_delete=models.CASCADE,
                                 related_name='regions')
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name='producers')

    class Meta:
        unique_together = (('producer', 'region',),)
        ordering = ('producer', 'region')

    def __str__(self):
        return f"{self.producer} ({self.region})"


class Grape(models.Model):
    GRAPE_TYPE_CHOICES = (
        ('white', 'White'),
        ('red', 'Red'),
    )
    name = models.CharField(max_length=100, unique=True)
    origin = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name='grapes',
                               null=True,
                               blank=True)
    type = models.CharField(max_length=5, choices=GRAPE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    """ vivino """
    # body
    # colour
    # acidity

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wines:grape_detail',
                       args=[self.id])


class Wine(models.Model):
    WINE_TYPE_CHOICES = (
        ('white', 'White'),
        ('red', 'Red'),
        ('rosé', 'Rosé'),
        ('sparkling', 'Sparkling'),
        # ('fortified', 'Fortified'),
        ('port', 'Port'),
        ('madeira', 'Madeira'),
        ('moscatel', 'Moscatel'),
    )
    name = models.CharField(max_length=100)
    producer = models.ForeignKey(
        Producer,
        on_delete=models.CASCADE,
        related_name='wines'
    )
    grape_varieties = models.ManyToManyField(Grape,
                                    through='WineGrape',
                                    through_fields=('wine', 'grape'))
    type = models.CharField(max_length=9, choices=WINE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    # style : tawny port
    # alcohol content : 20%

    # (vintage) year
    # tasting notes
    # production size
    # food pairings
    # updated_on
    # inserted_on

    class Meta:
        unique_together = (('name', 'producer', 'type',),)
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} ({self.type})"

    def get_absolute_url(self):
        return reverse('wines:wine_detail',
                       args=[self.id])


class WineGrape(models.Model):
    """ Intermediary table for the grape varieties that a wine is made of. """
    wine = models.ForeignKey(Wine,
                              on_delete=models.CASCADE,
                              related_name='grapes')
    grape = models.ForeignKey(Grape,
                              on_delete=models.CASCADE,
                              related_name='wines')

    class Meta:
        unique_together = (('wine', 'grape',),)
        ordering = ('wine', 'grape')

    def __str__(self):
        return f"{self.wine} ({self.grape})"


class Vintage(models.Model):
    wine = models.ForeignKey(Wine,
                             on_delete=models.CASCADE,
                             related_name='vintages')
    # null=True+blank=True allows the representation of N.V. (no vintage) wines
    year = models.SmallIntegerField(null=True,
                                    blank=True,
                                    validators=[MinValueValidator(1700),
                                                MaxValueValidator(2050)])
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (('wine', 'year',),)
        ordering = ('wine', 'year')

    def __str__(self):
        return f"{self.wine} ({self.year})"

    def get_absolute_url(self):
        return reverse('wines:vintage_detail',
                       args=[self.id])


class GrapeAlias(models.Model):
    name = models.CharField(max_length=100)
    grape = models.ForeignKey(Grape,
                              on_delete=models.CASCADE,
                              related_name='aliases')

    class Meta:
        unique_together = (('name', 'grape',),)
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} ({self.grape})"


class Review(models.Model):
    """ Model for wine reviews. """
    validators = [MinValueValidator(0), MaxValueValidator(10)]

    wine = models.ForeignKey(
        Wine,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    vintage = models.ForeignKey(
        Vintage,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(default=5, validators=validators)
    sweetness = models.PositiveSmallIntegerField(default=5, validators=validators)
    body = models.PositiveSmallIntegerField(default=5, validators=validators)
    acidity = models.PositiveSmallIntegerField(default=5, validators=validators)
    published_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        # A second constraint is needed since the first constraint isn't
        # enforced when vintage=None (i.e. a user would be able to write
        # multiple reviews for the same wine as long as those reviews didn't
        # refer a specific vintage
        constraints = [
            models.UniqueConstraint(fields=['wine', 'vintage', 'user'],
                                    name='wine_vintage_user_constraint'),
            models.UniqueConstraint(fields=['wine', 'user'],
                                    condition=models.Q(vintage=None),
                                    name='wine_user_vintagenull_constraint'),
        ]
        ordering = ('published_on',)

    def __str__(self):
        return f"{self.wine} review #{self.id}"

    def get_absolute_url(self):
        return reverse('wines:review_list',
                       args=[self.wine])


""" 
#####################################

Check this out before anything else:
    https://www.winesofportugal.com/en/travel-wine/wine-regions/

######################################

Nomenclatura comunitária de classificação dos vinhos VQPRD 
(Vinho de Qualidade Produzido em Região Determinada)

    https://pt.wikipedia.org/wiki/Denomina%C3%A7%C3%B5es_de_origem_portuguesas
    https://en.wikipedia.org/wiki/List_of_Portuguese_wine_regions

DOC: Denominação de Origem Controlada
IPR: Indicação de Proveniência Regulamentada
VR: Vinho regional
--: Vinho de mesa

class WineRegion(models.Model):
    name = models.CharField(max_length=100)
"""





