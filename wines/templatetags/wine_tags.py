from django import template

from ..forms import SearchForm, AdvancedWineSearchForm
from ..models import Wine, Vintage, Grape, Producer, Region, Review

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


@register.inclusion_tag('wines/search_bar.html')
def show_sitewide_search_form():
    search_form = SearchForm()
    return {"search_form": search_form}


@register.inclusion_tag('wines/wine/advanced_search_bar.html')
def show_wines_advanced_search_form():
    search_form = AdvancedWineSearchForm()
    return {"search_form": search_form}


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


@register.inclusion_tag('wines/latest_reviews.html')
def show_latest_reviews(count=5):
    latest_reviews = Review.objects.order_by('-published_on')[:count]
    return {"latest_reviews": latest_reviews}


@register.inclusion_tag('wines/last_visited_pages.html')
def show_last_visited_pages(request):
    last_visited = []
    pages = request.session.get("last_visited")
    if pages is not None:
        for page in pages:
            id = page['id']
            if page['type'] == 'wine':
                wine = Wine.objects.get(id=id)
                last_visited.append(wine)
            elif page['type'] == 'vintage':
                vintage = Vintage.objects.get(id=id)
                last_visited.append(vintage)
            elif page['type'] == 'grape':
                grape = Grape.objects.get(id=id)
                last_visited.append(grape)
            elif page['type'] == 'producer':
                producer = Producer.objects.get(id=id)
                last_visited.append(producer)
            elif page['type'] == 'region':
                region = Region.objects.get(id=id)
                last_visited.append(region)
    return {"last_visited_pages": last_visited}



""" Other tags """

# @register.simple_tag
# def other_wine_vintages(wine, vintage):
#     return wine.vintages.all.exclude(vintage=vintage)

