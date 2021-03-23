from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Wine, Grape, Producer, Region, Vintage
from .utils import paginator_helper


def wine_list(request):
    object_list = Wine.objects.all()
    paginator = Paginator(object_list, 10)
    wines = paginator_helper(request, paginator)
    return render(request,
                  'wines/wine/list.html',
                  {'wines': wines})


def wine_detail(request, id):
    wine = get_object_or_404(Wine, id=id)
    return render(request,
                  'wines/wine/detail.html',
                  {'wine': wine})


def vintage_list(request):
    object_list = Vintage.objects.all()
    paginator = Paginator(object_list, 10)
    vintages = paginator_helper(request, paginator)
    return render(request,
                  'wines/vintage/list.html',
                  {'vintages': vintages})


def vintage_detail(request, id):
    vintage = get_object_or_404(Vintage, id=id)
    return render(request,
                  'wines/vintage/detail.html',
                  {'vintage': vintage})


def grape_list(request):
    object_list = Grape.objects.all()
    paginator = Paginator(object_list, 10)
    grapes = paginator_helper(request, paginator)
    return render(request,
                  'wines/grape/list.html',
                  {'grapes': grapes})


def grape_detail(request, id):
    pass


def producer_list(request):
    object_list = Producer.objects.all()
    paginator = Paginator(object_list, 10)
    producers = paginator_helper(request, paginator)
    return render(request,
                  'wines/producer/list.html',
                  {'producers': producers})


def producer_detail(request, id):
    pass


def region_list(request):
    object_list = Region.objects.all()
    paginator = Paginator(object_list, 10)
    regions = paginator_helper(request, paginator)
    return render(request,
                  'wines/region/list.html',
                  {'regions': regions})


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