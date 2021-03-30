from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import ReviewForm
from .models import Wine, Grape, Producer, Region, Vintage, Review
from .utils import paginator_helper, session_updater


def wine_list(request):
    object_list = Wine.objects.all()
    paginator = Paginator(object_list, 10)
    wines = paginator_helper(request, paginator)
    return render(request,
                  'wines/wine/list.html',
                  {'wines': wines})


def wine_detail(request, id):
    wine = get_object_or_404(Wine, id=id)

    # update session data
    visited_page = {'type': 'wine', 'id': wine.id}
    session_updater(request, visited_page)

    print (request.session["last_visited"])

    # review handling
    new_review = None
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.wine = wine
            new_review.vintage = None
            new_review.user_id = request.user.id
            new_review.save()
            return redirect(wine)
    elif request.method == 'GET':
        # Show review form only if no generic review for this wine has been
        # written (i.e. show review form even if vintage specific reviews have
        # been written... does that make sense?)
        reviewed_already_by_this_user = Review.objects.filter(wine=wine,
                                                              user=request.user,
                                                              vintage=None).count()
        if not reviewed_already_by_this_user:
            review_form = ReviewForm()
        else:
            review_form = None

    return render(request,
                  'wines/wine/detail.html',
                  {'wine': wine,
                   'review_form': review_form,
                   'reviewed_already_by_this_user': reviewed_already_by_this_user})


def wines_per_type(request, type):
    object_list = Wine.objects.filter(type=type)
    paginator = Paginator(object_list, 10)
    wines = paginator_helper(request, paginator)
    return render(request,
                  'wines/wine/list.html',
                  {'wines': wines})


def wines_per_region(request, id):
    regions = Region.objects.filter(id=id)
    region_producers = Producer.objects.filter(Q(presence__in=regions) | Q(origin__in=regions))
    object_list = Wine.objects.filter(Q(producer__in=region_producers))
    paginator = Paginator(object_list, 10)
    wines = paginator_helper(request, paginator)
    return render(request,
                  'wines/wine/list.html',
                  {'wines': wines})


def vintage_list(request):
    object_list = Vintage.objects.all()
    paginator = Paginator(object_list, 10)
    vintages = paginator_helper(request, paginator)
    return render(request,
                  'wines/vintage/list.html',
                  {'vintages': vintages})


def vintage_detail(request, id):
    vintage = get_object_or_404(Vintage, id=id)

    # update session data
    visited_page = {'type': 'vintage', 'id': vintage.id}
    session_updater(request, visited_page)

    print (request.session["last_visited"])

    # review handling
    new_review = None
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.wine = vintage.wine
            new_review.vintage = vintage
            new_review.user_id = request.user.id
            new_review.save()
            return redirect(vintage)
    elif request.method == 'GET':
        # Show review form only if no review for this vintage has been written
        reviewed_already_by_this_user = Review.objects.filter(vintage=vintage,
                                                              user=request.user).count()
        if not reviewed_already_by_this_user:
            review_form = ReviewForm()
        else:
            review_form = None
    return render(request,
                  'wines/vintage/detail.html',
                  {'vintage': vintage,
                   'review_form': review_form,
                   'reviewed_already_by_this_user': reviewed_already_by_this_user})


def vintages_per_year(request, year):
    object_list = Vintage.objects.filter(year=year)
    paginator = Paginator(object_list, 10)
    vintages = paginator_helper(request, paginator)
    return render(request,
                  'wines/vintage/list.html',
                  {'vintages': vintages})


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


def grapes_per_type(request, type):
    object_list = Grape.objects.filter(type=type)
    paginator = Paginator(object_list, 10)
    grapes = paginator_helper(request, paginator)
    return render(request,
                  'wines/grape/list.html',
                  {'grapes': grapes})


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


def producers_per_region(request, id):
    regions = Region.objects.filter(id=id)
    object_list = Producer.objects.filter(Q(presence__in=regions) | Q(origin__in=regions))
    paginator = Paginator(object_list, 10)
    producers = paginator_helper(request, paginator)
    return render(request,
                  'wines/producer/list.html',
                  {'producers': producers})


def region_list(request):
    object_list = Region.objects.all()
    paginator = Paginator(object_list, 20)
    regions = paginator_helper(request, paginator)
    return render(request,
                  'wines/region/list.html',
                  {'regions': regions})


def region_detail(request, id):
    region = get_object_or_404(Region, id=id)
    return render(request,
                  'wines/region/detail.html',
                  {'region': region})


def wine_advanced_search(request):
    print(request.GET)
    results = Wine.objects.all()
    for k, v in request.GET.items():
        if k == 'name' and v:
            print('name')
            results = results.filter(Q(name__contains=v))
        elif k == 'type' and v:
            print('type')
            results = results.filter(Q(type=v))


    return render(request,
                  'wines/wine/advanced_search.html',
                  {'results': results})


def wine_search(request):
    search_string = request.GET.get("query")
    if search_string:
        results = Wine.objects.filter(Q(name__contains=search_string))
    else:
        results = None

    return render(request,
                  'wines/wine/search.html',
                  {'results': results})


def grape_search(request):
    search_string = request.GET.get("query")
    if search_string:
        results = Grape.objects.filter(Q(name__contains=search_string))
    else:
        results = None

    return render(request,
                  'wines/grape/search.html',
                  {'results': results})


def producer_search(request):
    search_string = request.GET.get("query")
    if search_string:
        results = Producer.objects.filter(Q(name__contains=search_string))
    else:
        results = None

    return render(request,
                  'wines/producer/search.html',
                  {'results': results})


def sitewide_search(request):
    search_string = request.GET.get("query")
    if search_string:
        wines = Wine.objects.filter(Q(name__contains=search_string))
        grapes = Grape.objects.filter(Q(name__contains=search_string))
        producers = Producer.objects.filter(Q(name__contains=search_string))
    else:
        wines = None
        grapes = None
        producers = None

    return render(request,
                  'wines/global_search.html',
                  {'wines': wines,
                   'grapes': grapes,
                   'producers': producers})


def landing_page(request):
    # # temporary hack
    # return redirect('wines/')
    return render(request,
                  'wines/landing_page.html')


