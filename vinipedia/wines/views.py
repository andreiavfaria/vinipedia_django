from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Wine


def wine_list(request):
    """ Returns a page with the list of inserted movies. """
    object_list = Wine.objects.all()
    paginator = Paginator(object_list, 5) # 10 movies in each page
    page = request.GET.get('page')
    try:
        wines = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        wines = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        wines = paginator.page(paginator.num_pages)
    return render(request,
                  'wines/movie/list.html',
                  {'wines': wines})


def wine_detail(request, id):
    """ Returns a page with the details for a specific movie. """
    wine = get_object_or_404(Wine, id=id)
    vintages = wine.vintages.all()
    return render(request,
                  'movies/movie/detail.html',
                  {'movie': wine,
                   'vintages': vintages})


def grape_list(request):
    pass


def grape_detail(request, id):
    pass


def producer_list(request):
    pass


def producer_detail(request, id):
    pass


def region_list(request):
    pass


def region_detail(request, id):
    pass


def wines_per_region(request, id):
    pass


def producers_per_region(request, id):
    pass


def vintages_per_year(request, year):
    pass


def wine_search(request):
    pass


def grape_search(request):
    pass


def producer_search(request):
    pass