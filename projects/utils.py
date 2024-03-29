from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Tag, Mod


def modPaginate(request, queryset, results):
    page = request.GET.get("page")
    paginator = Paginator(queryset, results)

    try:
        mods = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        mods = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages()
        mods = paginator.page(page)

    leftIndex = int(page) - 2

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 3

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return mods, custom_range


def modSearch(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
    tags = Tag.objects.filter(name__icontains=search_query)
    mods = Mod.objects.distinct().filter(
        Q(title__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(owner__name__icontains=search_query)
        | Q(tags__in=tags)
    )
    return mods, search_query
