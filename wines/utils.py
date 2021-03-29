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


def session_updater(request, visited_page):
    """ Abstracts the repeated logic for updating sessions inside the views. """
    # Gets the last_visited session key if it exists, creating it otherwise
    last_visited = request.session.get("last_visited", [])
    if visited_page in last_visited:
        last_visited = list(filter(lambda x: x != visited_page, last_visited))
    last_visited.insert(0, visited_page)
    last_visited = last_visited[:10]
    request.session["last_visited"] = last_visited
    request.session.modified = True