from django import forms


# class ReviewForm(forms.ModelForm):
#
#     class Meta:
#         model = Review
#         fields = ('score', 'body')


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='')

