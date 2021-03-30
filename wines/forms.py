from django import forms

from .models import Review, Wine


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
                           widget=forms.Select(choices=Wine.WINE_TYPE_CHOICES))
    # producer
    # grape varieties
    # vintage = forms.IntegerField(max_length=100, label='')
    # average score
    # alcohol content
    # with grape / without grape
    # from producer / not from producer
    # type

