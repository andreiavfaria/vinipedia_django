from django import forms

from .models import Review


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

