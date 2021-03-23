from django import template

from ..forms import SearchForm
from ..models import Wine, Vintage, Grape, Producer

register = template.Library()


""" Simple tags """


@register.simple_tag
def total_wines_registered():
    return Wine.objects.count()


@register.simple_tag
def total_vintages_registered():
    return Vintage.objects.count()


@register.simple_tag
def total_grapes_registered():
    return Grape.objects.count()


@register.simple_tag
def total_producers_registered():
    return Producer.objects.count()


# @register.simple_tag
# def total_reviews_written():
#     return Review.objects.count()


""" Search bar inclusion tags """


@register.inclusion_tag('wines/wine/search_bar.html')
def show_wines_search_form():
    search_form = SearchForm()
    return {"search_form": search_form}


@register.inclusion_tag('wines/grape/search_bar.html')
def show_grapes_search_form():
    search_form = SearchForm()
    return {"search_form": search_form}


@register.inclusion_tag('wines/producer/search_bar.html')
def show_producers_search_form():
    search_form = SearchForm()
    return {"search_form": search_form}

