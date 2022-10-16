from .models import Skill, Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def profilesPaginate(request, queryset, results):
    page = request.GET.get('page')
    paginator = Paginator(queryset, results)

    try:
        moders = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        moders  = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages()
        moders  = paginator.page(page)

    leftIndex = (int(page) - 2)

    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 3)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+1
    
    custom_range = range(leftIndex, rightIndex)

    return moders, custom_range


def profilesearch(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains = search_query)
    moders = Profile.objects.distinct().filter(Q(name__icontains=search_query) |
                                    Q(short_intro__icontains=search_query) |
                                    Q(skill__in=skills)
    )
    if not search_query:
        res = []
        for i in moders:
            if i.mod_set.all():
                    res.append(i)
        return res, search_query


    
    return moders, search_query