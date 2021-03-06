from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Avg, Count, F
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
        if request.user.is_authenticated:
            # Show review form only if no generic review for this wine has been
            # written (i.e. show review form even if vintage specific reviews have
            # been written... does that make sense?)
            reviewed_already_by_this_user = Review.objects.filter(wine=wine,
                                                                  user=request.user,
                                                                  vintage=None).count()
        else:
            reviewed_already_by_this_user = None
        if not reviewed_already_by_this_user:
            review_form = ReviewForm()
        else:
            review_form = None

    return render(request,
                  'wines/wine/detail.html',
                  {'wine': wine,
                   'review_form': review_form,
                   'reviewed_already_by_this_user': reviewed_already_by_this_user,
                   'new_review': new_review})


def wines_per_type(request, type):
    object_list = Wine.objects.filter(type=type)
    paginator = Paginator(object_list, 10)
    wines = paginator_helper(request, paginator)
    print(request.GET)
    return render(request,
                  'wines/wine/list_per_type.html',
                  {'wines': wines,
                   'type': type})


def wines_per_region(request, id):
    region = get_object_or_404(Region, id=id)
    region_producers = Producer.objects.filter(Q(presence=region) | Q(origin=region))
    object_list = Wine.objects.filter(Q(producer__in=region_producers))
    paginator = Paginator(object_list, 10)
    wines = paginator_helper(request, paginator)
    return render(request,
                  'wines/wine/list_per_region.html',
                  {'wines': wines,
                   'name': region.name})


def wines_per_grape(request, id):
    grape = get_object_or_404(Grape, id=id)
    object_list = Wine.objects.filter(grape_varieties=grape)
    paginator = Paginator(object_list, 10)
    wines = paginator_helper(request, paginator)
    return render(request,
                  'wines/wine/list_per_grape.html',
                  {'wines': wines,
                   'name': grape.name})


def wines_per_producer(request, id):
    producer = get_object_or_404(Producer, id=id)
    object_list = Wine.objects.filter(producer=producer)
    paginator = Paginator(object_list, 10)
    wines = paginator_helper(request, paginator)
    return render(request,
                  'wines/wine/list_per_producer.html',
                  {'wines': wines,
                   'producer': producer})


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
        if request.user.is_authenticated:
            # Show review form only if no review for this vintage has been written
            reviewed_already_by_this_user = Review.objects.filter(vintage=vintage,
                                                                  user=request.user).count()
        else:
            reviewed_already_by_this_user = None
        if not reviewed_already_by_this_user:
            review_form = ReviewForm()
        else:
            review_form = None
    return render(request,
                  'wines/vintage/detail.html',
                  {'vintage': vintage,
                   'review_form': review_form,
                   'reviewed_already_by_this_user': reviewed_already_by_this_user,
                   'new_review': new_review})


def vintages_per_wine(request, id):
    wine = get_object_or_404(Wine, id=id)
    object_list = Vintage.objects.filter(wine=wine)
    paginator = Paginator(object_list, 10)
    vintages = paginator_helper(request, paginator)
    return render(request,
                  'wines/vintage/list_per_wine.html',
                  {'vintages': vintages,
                   'name': wine.name})


def vintages_per_grape(request, id):
    grape = get_object_or_404(Grape, id=id)
    object_list = Vintage.objects.filter(wine__grape_varieties=grape)
    paginator = Paginator(object_list, 10)
    vintages = paginator_helper(request, paginator)
    return render(request,
                  'wines/vintage/list_per_grape.html',
                  {'vintages': vintages,
                   'name': grape.name})


def vintages_per_producer(request, id):
    producer = get_object_or_404(Producer, id=id)
    object_list = Vintage.objects.filter(wine__producer=producer)
    paginator = Paginator(object_list, 10)
    vintages = paginator_helper(request, paginator)
    return render(request,
                  'wines/vintage/list_per_producer.html',
                  {'vintages': vintages,
                   'producer': producer})


def vintages_per_region(request, id):
    region = get_object_or_404(Region, id=id)
    object_list = Vintage.objects.filter(wine__origin=region)
    paginator = Paginator(object_list, 10)
    vintages = paginator_helper(request, paginator)
    return render(request,
                  'wines/vintage/list_per_region.html',
                  {'vintages': vintages,
                   'name': region.name})


def vintages_per_year(request, year):
    object_list = Vintage.objects.filter(year=year)
    paginator = Paginator(object_list, 10)
    vintages = paginator_helper(request, paginator)
    return render(request,
                  'wines/vintage/list_per_year.html',
                  {'vintages': vintages,
                   'year': year})


def grape_list(request):
    object_list = Grape.objects.all()
    paginator = Paginator(object_list, 10)
    grapes = paginator_helper(request, paginator)
    return render(request,
                  'wines/grape/list.html',
                  {'grapes': grapes})


def grape_detail(request, id):
    grape = get_object_or_404(Grape, id=id)

    # update session data
    visited_page = {'type': 'grape', 'id': grape.id}
    session_updater(request, visited_page)

    return render(request,
                  'wines/grape/detail.html',
                  {'grape': grape})


def grapes_per_type(request, type):
    object_list = Grape.objects.filter(type=type)
    paginator = Paginator(object_list, 10)
    grapes = paginator_helper(request, paginator)
    return render(request,
                  'wines/grape/list_per_type.html',
                  {'grapes': grapes,
                   'type': type})


def producer_list(request):
    object_list = Producer.objects.all()
    paginator = Paginator(object_list, 10)
    producers = paginator_helper(request, paginator)
    return render(request,
                  'wines/producer/list.html',
                  {'producers': producers})


def producer_detail(request, id):
    producer = get_object_or_404(Producer, id=id)

    # update session data
    visited_page = {'type': 'producer', 'id': producer.id}
    session_updater(request, visited_page)

    return render(request,
                  'wines/producer/detail.html',
                  {'producer': producer})


def producers_per_region(request, id):
    region = get_object_or_404(Region, id=id)
    # hack using distinct() to remove duplicates, since the following query is
    # returning duplicate entries somehow:
    #   Producer.objects.filter(Q(origin=region) | Q(presence=region))
    object_list = Producer.objects.filter(Q(presence=region) | Q(origin=region)).distinct()
    paginator = Paginator(object_list, 10)
    producers = paginator_helper(request, paginator)
    return render(request,
                  'wines/producer/list_per_region.html',
                  {'producers': producers,
                   'name': region.name})


def region_list(request):
    object_list = Region.objects.all()
    paginator = Paginator(object_list, 20)
    regions = paginator_helper(request, paginator)
    return render(request,
                  'wines/region/list.html',
                  {'regions': regions})


def region_detail(request, id):
    region = get_object_or_404(Region, id=id)

    # update session data
    visited_page = {'type': 'region', 'id': region.id}
    session_updater(request, visited_page)

    return render(request,
                  'wines/region/detail.html',
                  {'region': region})


def wine_advanced_search(request):
    if not request.GET:
        results = None
    else:
        results = Wine.objects.all()
        for k, v in request.GET.items():
            if k == 'name' and v:
                results = results.filter(Q(name__icontains=v))
            elif k == 'type':
                results = results.filter(Q(type__in=request.GET.getlist(k)))
            elif k == 'producer':
                results = results.filter(Q(producer__in=request.GET.getlist(k)))
            elif k == 'grape_varieties':
                results = results.filter(Q(grape_varieties__in=request.GET.getlist(k)))
            elif k == 'average_score' and v:
                wines_with_avg_rating = Review.objects.all().select_related('wine') \
                                        .values('wine_id') \
                                        .annotate(avg_score=Avg('score'), nr_reviews=Count('wine_id')) \
                                        .order_by('avg_score')\
                                        .filter(Q(avg_score__gte=v)) \
                                        .values('wine_id')
                results = results.filter(Q(pk__in=wines_with_avg_rating))
            # Make sure 'vintage_year' is the last elif condition
            elif k == 'vintage_year' and v:
                vintages = Vintage.objects.filter(year=v, wine__in=results)
                results = vintages

    return render(request,
                  'wines/wine/advanced_search.html',
                  {'results': results})


def wine_search(request):
    search_string = request.GET.get("query")
    if search_string:
        results = Wine.objects.filter(Q(name__icontains=search_string))
    else:
        results = None

    return render(request,
                  'wines/wine/search.html',
                  {'results': results})


def grape_search(request):
    search_string = request.GET.get("query")
    if search_string:
        results = Grape.objects.filter(Q(name__icontains=search_string))
    else:
        results = None

    return render(request,
                  'wines/grape/search.html',
                  {'results': results})


def producer_search(request):
    search_string = request.GET.get("query")
    if search_string:
        results = Producer.objects.filter(Q(name__icontains=search_string))
    else:
        results = None

    return render(request,
                  'wines/producer/search.html',
                  {'results': results})


def sitewide_search(request):
    search_string = request.GET.get("query")
    if search_string:
        wines = Wine.objects.filter(Q(name__icontains=search_string))
        grapes = Grape.objects.filter(Q(name__icontains=search_string))
        producers = Producer.objects.filter(Q(name__icontains=search_string))
    else:
        wines = None
        grapes = None
        producers = None

    return render(request,
                  'wines/global_search.html',
                  {'wines': wines,
                   'grapes': grapes,
                   'producers': producers})


def homepage(request):
    top_rated_wines = Wine.objects.annotate(avg_rating=Avg('reviews__score')).order_by(F('avg_rating').desc(nulls_last=True))[:5]
    top_rated_vintages = Vintage.objects.annotate(avg_rating=Avg('reviews__score')).order_by(F('avg_rating').desc(nulls_last=True))[:5]
    red_wines = Wine.objects.filter(type='red').order_by('?')[:5]
    white_wines = Wine.objects.filter(type='white').order_by('?')[:5]
    fortified_wines = Wine.objects.filter(type__in=('port', 'moscatel', 'madeira')).order_by('?')[:5]
    other_wines = Wine.objects.filter(type__in=('ros??', 'sparkling')).order_by('?')[:5]
    return render(request,
                  'wines/homepage.html',
                  {'top_rated_wines': top_rated_wines,
                   'top_rated_vintages': top_rated_vintages,
                   'red_wines': red_wines,
                   'white_wines': white_wines,
                   'fortified_wines': fortified_wines,
                   'other_wines': other_wines})


