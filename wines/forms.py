from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Review, Wine, Producer, Grape


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('score',
                  'body',
                  'sweetness',
                  'acidity',
                  'tannin',
                  'text')


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='')


class AdvancedWineSearchForm(forms.Form):

    name = forms.CharField(required=False)
    type = forms.CharField(max_length=9,
                           required=False,
                           widget=forms.SelectMultiple(choices=Wine.WINE_TYPE_CHOICES))
    producer = forms.ModelMultipleChoiceField(queryset=Producer.objects.all(),
                                              # empty_label="--------",
                                              required=False)
    grape_varieties = forms.ModelMultipleChoiceField(queryset=Grape.objects.all(),
                                                     # empty_label="--------",
                                                     required=False)
    average_score = forms.FloatField(required=False,
                                     validators=[MinValueValidator(0),
                                                 MaxValueValidator(5)])
    vintage_year = forms.IntegerField(required=False,
                                      validators=[MinValueValidator(1700),
                                                  MaxValueValidator(2050)])
    # year / vintage
    # alcohol content
    # with grape / without grape
    # from producer / not from producer

