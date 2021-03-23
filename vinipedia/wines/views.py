from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
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
    grape = get_object_or_404(Grape, id=id)
    return render(request,
                  'wines/grape/detail.html',
                  {'grape': grape})


def producer_list(request):
    object_list = Producer.objects.all()
    paginator = Paginator(object_list, 10)
    producers = paginator_helper(request, paginator)
    return render(request,
                  'wines/producer/list.html',
                  {'producers': producers})


def producer_detail(request, id):
    producer = get_object_or_404(Producer, id=id)
    return render(request,
                  'wines/producer/detail.html',
                  {'producer': producer})


def region_list(request):
    object_list = Region.objects.all()
    paginator = Paginator(object_list, 10)
    regions = paginator_helper(request, paginator)
    return render(request,
                  'wines/region/list.html',
                  {'regions': regions})


def region_detail(request, id):
    region = get_object_or_404(Region, id=id)
    return render(request,
                  'wines/region/detail.html',
                  {'region': region})


def wines_per_region(request, id):
    pass


def producers_per_region(request, id):
    pass


def vintages_per_year(request, year):
    pass


def wine_search(request):
    search_string = request.GET.get("query")
    if search_string:
        results = Wine.objects.filter(Q(name__contains=search_string) | Q(description__contains=search_string))
    else:
        results = None

    return render(request,
                 'wines/wine/search.html',
                 {'results': results})


def grape_search(request):
    search_string = request.GET.get("query")
    if search_string:
        results = Grape.objects.filter(Q(name__contains=search_string) | Q(description__contains=search_string))
    else:
        results = None

    return render(request,
                 'wines/grape/search.html',
                 {'results': results})


def producer_search(request):
    search_string = request.GET.get("query")
    if search_string:
        results = Producer.objects.filter(Q(name__contains=search_string) | Q(description__contains=search_string))
    else:
        results = None

    return render(request,
                 'wines/producer/search.html',
                 {'results': results})