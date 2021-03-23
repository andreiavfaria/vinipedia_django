from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginator_helper(request, paginator):
    """ Abstracts the repeated paginator logic inside the views. """
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        objects = paginator.page(paginator.num_pages)
    return objects

