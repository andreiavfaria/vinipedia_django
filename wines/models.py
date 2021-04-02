from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db.models import Avg
from django.urls import reverse


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='countries/%Y/%m/%d/', null=True, blank=True)

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
    image = models.ImageField(upload_to='regions/%Y/%m/%d/', null=True, blank=True)

    def get_other_producers(self):
        """ Returns the non-local producers that operate in the region.

        (e.g. Bacalhôa, which is from Setúbal but also operates in Alentejo.

        """
        other_producers = Producer.objects.filter(presence=self.pk).exclude(origin=self.pk)
        return other_producers

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
    short_name = models.CharField(max_length=50, unique=True, null=True)
    origin = models.ForeignKey(Region,
                               on_delete=models.RESTRICT,
                               related_name='local_producers')
    presence = models.ManyToManyField(Region,
                                      through='ProducerRegion',
                                      through_fields=('producer', 'region'))
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='producers/%Y/%m/%d/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    # phone
    # social media

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

    class Body(models.IntegerChoices):
        VERY_LIGHT = 1
        LIGHT = 2
        MEDIUM = 3
        BOLD = 4
        VERY_BOLD = 5

    class Acidity(models.IntegerChoices):
        VERY_SOFT = 1
        SOFT = 2
        MEDIUM = 3
        ACIDIC = 4
        VERY_ACIDIC = 5

    class Colour(models.IntegerChoices):
        STRAW = 1
        YELLOW = 2
        GOLD = 3
        BROWN = 4
        AMBER = 5
        COPPER = 6
        SALMON = 7
        PINK = 8
        RUBY = 9
        PURPLE = 10
        GARNET = 11
        TAWNY = 12

    GRAPE_TYPE_CHOICES = (
        ('white', 'White'),
        ('red', 'Red'),
    )
    name = models.CharField(max_length=100, unique=True)
    origin = models.ForeignKey(Region,
                               on_delete=models.RESTRICT,
                               related_name='grapes',
                               null=True,
                               blank=True)
    type = models.CharField(max_length=5, choices=GRAPE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='grapes/%Y/%m/%d/', null=True, blank=True)
    # colour = models.IntegerField(choices=Colour.choices, null=True)
    body = models.IntegerField(choices=Body.choices, null=True)
    acidity = models.IntegerField(choices=Acidity.choices, null=True)

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
        on_delete=models.RESTRICT,
        related_name='wines'
    )
    grape_varieties = models.ManyToManyField(Grape,
                                    through='WineGrape',
                                    through_fields=('wine', 'grape'))
    type = models.CharField(max_length=9, choices=WINE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='wines/%Y/%m/%d/', null=True, blank=True)
    origin = models.ForeignKey(Region,
                               on_delete=models.RESTRICT,
                               related_name='local_wines')

    def get_average_rating(self):
        """ Returns the consolidated average review rating for a wine
        (including every review for each of its vintages). """
        average_rating = Review.objects.filter(wine=self.pk).aggregate(Avg('score'))['score__avg']
        if average_rating:
            return round(average_rating, 1)
        return None

    class Meta:
        unique_together = (('name', 'type', 'producer',),)
        ordering = ('name',)

    def save(self, *args, **kwargs):
        # Ensure the wine's origin matches its producer's origin or presence
        # (we override the model's save method since this constraint apparently
        # can't be implemented using pure Django model constraints)
        producer_operating_in_this_region = self.producer.regions.filter(region=self.origin).count()
        if self.origin != self.producer.origin and not producer_operating_in_this_region:
            raise Exception("The wine origin must match the producer's origin or regional presence.")
        super(Wine, self).save(*args, **kwargs)

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
    image = models.ImageField(upload_to='vintages/%Y/%m/%d/', null=True, blank=True)
    alcohol_content = models.FloatField(null=True, blank=True,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(100)])
    # production size
    # tasting notes
    # food pairings
    # updated_on
    # inserted_on

    def get_average_rating(self):
        """ Returns the average review rating for a vintage. """
        average_rating = Review.objects.filter(vintage=self.pk).aggregate(Avg('score'))['score__avg']
        if average_rating:
            return round(average_rating, 1)
        return None

    def get_average_body(self):
        reviews_with_body_score = Review.objects.filter(vintage=self.pk).exclude(body=None)
        if reviews_with_body_score:
            avg = Review.objects.filter(vintage=self.pk).aggregate(Avg('body'))['body__avg']
            return round(avg, 1)
        return None

    def get_average_sweetness(self):
        reviews_with_sweetness_score = Review.objects.filter(vintage=self.pk).exclude(sweetness=None)
        if reviews_with_sweetness_score:
            avg = Review.objects.filter(vintage=self.pk).aggregate(Avg('sweetness'))['sweetness__avg']
            return round(avg, 1)
        return None

    def get_average_acidity(self):
        reviews_with_acidity_score = Review.objects.filter(vintage=self.pk).exclude(acidity=None)
        if reviews_with_acidity_score:
            avg = Review.objects.filter(vintage=self.pk).aggregate(Avg('acidity'))['acidity__avg']
            return round(avg, 1)
        return None

    def get_average_tannin(self):
        reviews_with_tannin_score = Review.objects.filter(vintage=self.pk).exclude(tannin=None)
        if reviews_with_tannin_score:
            avg = Review.objects.filter(vintage=self.pk).aggregate(Avg('tannin'))['tannin__avg']
            return round(avg, 1)
        return None

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
    # region/country

    class Meta:
        unique_together = (('name', 'grape',),)
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} ({self.grape})"


class Review(models.Model):
    """ Model for wine reviews. """
    validators = [MinValueValidator(1), MaxValueValidator(5)]

    class Sweetness(models.IntegerChoices):
        VERY_DRY = 1
        DRY = 2
        MEDIUM = 3
        SWEET = 4
        VERY_SWEET = 5

    class Body(models.IntegerChoices):
        VERY_LIGHT = 1
        LIGHT = 2
        MEDIUM = 3
        BOLD = 4
        VERY_BOLD = 5

    class Acidity(models.IntegerChoices):
        VERY_SOFT = 1
        SOFT = 2
        MEDIUM = 3
        ACIDIC = 4
        VERY_ACIDIC = 5

    class Tannin(models.IntegerChoices):
        VERY_SMOOTH = 1
        SMOOTH = 2
        MEDIUM = 3
        TANNIC = 4
        VERY_TANNIC = 5

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
    score = models.PositiveSmallIntegerField(default=3, validators=validators)
    sweetness = models.IntegerField(choices=Sweetness.choices, null=True)
    body = models.IntegerField(choices=Body.choices, null=True)
    acidity = models.IntegerField(choices=Acidity.choices, null=True)
    tannin = models.IntegerField(choices=Tannin.choices, null=True)
    published_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    # taste

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

    def save(self, *args, **kwargs):
        # Ensure that (if vintage != null) the selected vintage corresponds to
        # the selected wine.
        # (we override the model's save method since this constraint apparently
        # can't be implemented using pure Django model constraints)
        if self.vintage is not None and self.vintage.wine != self.wine:
            raise Exception("The selected vintage must correspond to the selected wine.")
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        if self.vintage:
            return f"{self.vintage} review #{self.id}"
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





