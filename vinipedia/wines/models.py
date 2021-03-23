from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('-name',)

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
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    origin = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name='producers')
    presence = models.ManyToManyField(Region,
                                      through='ProducerRegion',
                                      through_fields=('producer', 'region'))
    description = models.TextField(blank=True)
    # ^^^^ country (derived from region)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProducerRegion(models.Model):
    """ Intermediary table for the regions where a producer operates.

        (Bacalhôa Vinhos de Portugal, for instance, operates in 7 different
        regions)

    """
    producer = models.ForeignKey(Producer,
                                 on_delete=models.CASCADE,
                                 related_name='producers')
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name='regions')

    class Meta:
        unique_together = (('producer', 'region',),)
        ordering = ('-producer', '-region')

    def __str__(self):
        return f"{self.producer} ({self.region})"


class Grape(models.Model):
    GRAPE_TYPE_CHOICES = (
        ('white', 'White'),
        ('red', 'Red'),
    )
    name = models.CharField(max_length=100, unique=True)
    """ vivino """
    origin = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name='grapes',
                               null=True,
                               blank=True)
    grape_type = models.CharField(max_length=5, choices=GRAPE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    # body
    # colour
    # acidity
    # description

    # type = models.ForeignKey(Director,
    #                                  on_delete=models.CASCADE,
    #                                  related_name='movies')

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Wine(models.Model):
    name = models.CharField(max_length=100)
    """ vivino """
    # producer / winery : taylor's
    producer = models.ForeignKey(
        Producer,
        on_delete=models.CASCADE,
        related_name='wines'
    )
    # grape varieties / grapes : touriga nacional, tinta roriz, touriga francesa
    grapes = models.ManyToManyField(Grape,
                                    through='WineGrape',
                                    through_fields=('wine', 'grape'))
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
        unique_together = (('name', 'producer',),)
        ordering = ('-name',)

    def __str__(self):
        return self.name


class WineGrape(models.Model):
    """ Intermediary table for the grape varieties that a wine is made of. """
    wine = models.ForeignKey(Wine,
                              on_delete=models.CASCADE,
                              related_name='wines')
    grape = models.ForeignKey(Grape,
                              on_delete=models.CASCADE,
                              related_name='grapes')

    class Meta:
        unique_together = (('wine', 'grape',),)
        ordering = ('-wine', '-grape')

    def __str__(self):
        return f"{self.wine} ({self.grape})"


class Vintage(models.Model):
    wine = models.ForeignKey(Wine,
                             on_delete=models.CASCADE,
                             related_name='vintages')
    year = models.SmallIntegerField(validators=[MinValueValidator(1700),
                                                MaxValueValidator(2050)])
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (('wine', 'year',),)
        ordering = ('-wine', '-year')

    def __str__(self):
        return f"{self.wine} ({self.year})"


class GrapeAlias(models.Model):
    name = models.CharField(max_length=100)
    grape = models.ForeignKey(Grape,
                              on_delete=models.CASCADE,
                              related_name='aliases')

    class Meta:
        unique_together = (('name', 'grape',),)
        ordering = ('-name',)

    def __str__(self):
        return f"{self.name} ({self.grape})"


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





