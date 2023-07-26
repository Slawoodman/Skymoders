from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import FriendRequest, FriendList
from users.models import Profile
from itertools import chain


def get_frine_requet_or_false(sender, receiver):
    try:
        return FriendRequest.objects.get(
            sender=sender, receiver=receiver, is_active=True
        )
    except:
        return False


def profilesPaginate(request, queryset, results):
    page = request.GET.get("page")
    paginator = Paginator(queryset, results)

    try:
        moders = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        moders = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages()
        moders = paginator.page(page)

    leftIndex = int(page) - 2

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 3

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return moders, custom_range


def profilesearch(request, flag=False, user_id=None):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    if flag:
        is_self = True
        user_friends = []
        profile = Profile.objects.get(pk=user_id)
        friends = FriendList.objects.get(user=profile.user).friends.all()
        if request.user != profile.user:
            is_self = False
            user_friends = FriendList.objects.get(user=request.user).friends.all()
        if search_query:
            friends = Profile.objects.distinct().filter(
                Q(username__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(short_intro__icontains=search_query)
            )
        requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)
        sent_requests = FriendRequest.objects.filter(
            sender=request.user, is_active=True
        )
        requests = list(chain(requests, sent_requests))
        print(requests)
        return friends, user_friends, search_query, is_self, requests

    requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)
    requests = requests.distinct().filter(Q(sender__username__icontains=search_query))
    print(requests)
    if not search_query:
        res = []
        for i in requests:
            res.append(i)
        return res, search_query

    return requests, search_query
