from django.shortcuts import render, redirect
from .models import FriendList, FriendRequest
from users.models import Profile
from django.contrib.auth.decorators import login_required
from .utils import profilesPaginate, profilesearch
from django.contrib import messages
from urllib.parse import urlparse, parse_qs


@login_required(login_url="login-user")
def send_friend_request(request, pk):
    previous_path = request.META.get("HTTP_REFERER")
    user = request.user
    receiver = Profile.objects.get(pk=pk)
    # print(receiver)
    if receiver:
        receiver = receiver.user
        friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
        # print(friend_requests)
        if friend_requests:
            # print(friend_requests)
            for requ in friend_requests:
                if requ.is_active:
                    messages.error(request, "You already sent them a friend request.")
                    # print("You already sent them a friend request.")
                    return redirect(previous_path)
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                messages.success(request, "Friend request sent.")
                # print("Friend request sent.")
        else:
            friend_request = FriendRequest(sender=user, receiver=receiver)
            friend_request.save()
            messages.success(request, "Friend request sent.")
            # print("Friend request sent.")
    return redirect(previous_path)


@login_required(login_url="login-user")
def show_requests(request):
    friend_requests, search_query = profilesearch(request)
    friend_requests, custom_range = profilesPaginate(request, friend_requests, 6)
    context = {
        "friend_requests": friend_requests,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "friends/request.html", context)


@login_required(login_url="login-user")
def accept_friend_request(request, pk):
    previous_path = request.META.get("HTTP_REFERER")
    try:
        friend_request = FriendRequest.objects.get(pk=pk)
        if friend_request.receiver == request.user:
            try:
                friend_request.accept()
                messages.success(request, "Friend request accepted")

            except:
                messages.error(request, "Something went wrong.")
        else:
            messages.error(request, "That is not your request to accept.")
    except:
        messages.error(request, "Friend request is't accessible")
    # print(friend_request, pk)
    return redirect(previous_path)


@login_required(login_url="login-user")
def unfriend_user(request, pk):
    previous_path = request.META.get("HTTP_REFERER")
    parsed_url = urlparse(previous_path)
    next_url = parse_qs(parsed_url.query).get("next", [""])[0]

    user = request.user
    removee = Profile.objects.get(pk=pk)
    friend_list = FriendList.objects.get(user=user)

    if request.method == "POST":
        try:
            friend_list.unfriend(removee.user)
            messages.success(request, "Successfully removed that friend.")
            return redirect(next_url)
        except:
            messages.error(request, "Something went wrong.")
            return redirect(next_url)
    context = {"obj": removee.user, "page": "unfriend"}
    return render(request, "delete.html", context)


@login_required(login_url="login-user")
def decline_friend(request, pk):
    previous_path = request.META.get("HTTP_REFERER")
    parsed_url = urlparse(previous_path)
    next_url = parse_qs(parsed_url.query).get("next", [""])[0]

    context = {}

    try:
        friend_request = FriendRequest.objects.get(pk=pk)
        if request.method == "POST":
            if friend_request.receiver == request.user:
                try:
                    friend_request.decline()
                    messages.success(request, "Friend request declined")
                    return redirect(next_url)
                except:
                    messages.error(request, "Something went wrong.")
                    return redirect(next_url)
            else:
                messages.error(request, "That is not your request to decline")
                return redirect(next_url)
    except:
        messages.error(request, "Friend request is't accessible.")
        return redirect(next_url)
    context["page"] = "decline"
    context["obj"] = friend_request.receiver
    return render(request, "delete.html", context)


@login_required(login_url="login-user")
def cancel_friend(request, pk):
    previous_path = request.META.get("HTTP_REFERER")
    parsed_url = urlparse(previous_path)
    next_url = parse_qs(parsed_url.query).get("next", [""])[0]

    context = {}
    try:
        receiver = Profile.objects.get(pk=pk).user
        try:
            friend_request = FriendRequest.objects.filter(
                receiver=receiver, sender=request.user, is_active=True
            )
            if request.method == "POST":
                print(friend_request)
                if len(friend_request) > 1:
                    for req in friend_request:
                        req.cancel()
                        req.delete()
                else:
                    friend_request.first().cancel()
                    friend_request.first().delete()
                messages.success(request, "Friend request is canceled")
                return redirect(next_url)
        except:
            messages.error(request, "Friend request is't accessible.")
            return redirect(next_url)
    except:
        messages.error(request, "Unable to cancel friend request.")
        return redirect(next_url)

    context["page"] = "cancel"
    context["obj"] = receiver
    return render(request, "delete.html", context)


@login_required(login_url="login-user")
def friend_list(request, user_id):
    page = request.build_absolute_uri()
    profile = Profile.objects.get(pk=user_id)
    friend_for_user = FriendList.objects.get(user=request.user).friends.all()
    friends, user_friends, search_query, is_self, friend_request = profilesearch(
        request, flag=True, user_id=user_id
    )
    friends, custom_range = profilesPaginate(request, friends, 6)
    context = {
        "page": "friend_page",
        "friends": friends,
        "user_friends": user_friends,
        "friend_for_user": friend_for_user,
        "is_self": is_self,
        "search_query": search_query,
        "moder": profile.user,
        "custom_range": custom_range,
        "friend_request": friend_request,
        "prev_page": page,
    }
    print(context)

    return render(request, "friends/friends.html", context)
