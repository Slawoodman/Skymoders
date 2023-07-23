from django.shortcuts import render, redirect
from .models import FriendList, FriendRequest
from users.models import Profile
from django.contrib.auth.decorators import login_required
from .fin_re import FriendRequestStatus
from .utils import get_frine_requet_or_false, profilesPaginate, profilesearch
from django.http import HttpResponse
import json
from django.contrib import messages


@login_required(login_url='login-user')
def friendspage(request, pk):
    context = {}
    moder = Profile.objects.get(id=pk)
    specSkill = moder.skill_set.exclude(description__exact="")
    addSkill = moder.skill_set.filter(description="")
    context["addskills"] = addSkill
    context["moder"] = moder
    context["moder_id"]  = moder.id 
    context["specSkill"] = specSkill
    
    try:
        fiendListr = FriendList.objects.get(user=request.user)
    except:
        fiendListr = FriendList(user=request.user)
        fiendListr.save()
    
    friends = fiendListr.friends.all()
    # print(friends)
    is_self = True
    is_friend = False
    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    friend_requests = None
    user = request.user

    fried =  FriendList.objects.get(user=moder.user).friends.all()
    print(len(FriendList.objects.get(user=moder.user).friends.all()))

    context["acc_friends"] = len(fried)
    context["friends"] = friends

    if user.is_authenticated and user != moder.user:
        
        is_self = False
        if friends.filter(pk=moder.user.id):
            # print(f"{request.user} friend with {friends.get(pk=moder.user.id)}")
            is_friend = True
        else:
            if get_frine_requet_or_false(sender=moder.user, receiver=user) != False:
                request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
            elif get_frine_requet_or_false(sender=user, receiver=moder.user) != False:
                request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
            else:
                request_sent =  FriendRequestStatus.NO_REQUEST_SENT.value
    
    elif not user.is_authenticated:
        is_self = False
        
    else:
        try:
            friend_requests = FriendRequest.objects.filter(receiver=moder.user, is_active=True)
        except:
            pass
    context['is_friend'] = is_friend
    context['is_self'] = is_self
    context['friend_requests'] = friend_requests
    context['request_sent'] = request_sent
    try:
        rqst = FriendRequest.objects.get(sender=moder.user,receiver=user, is_active=True)
        context['request_id'] = rqst.id
    except:
        pass
    print(context)
    return render(request, 'friends/friend.html', context)


@login_required(login_url='login-user')
def send_friend_request(request, pk):
    previous_path = request.META.get('HTTP_REFERER')
    user = request.user
    receiver = Profile.objects.get(pk=pk)
    print(receiver)
    if receiver:
        receiver = receiver.user
        friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
        print(friend_requests)
        if friend_requests:
            print(friend_requests)
            #после того как убали фриенд рекест, и его всерано показыает тпиа как
            for requ in friend_requests:
                if requ.is_active:
                    messages.error(request, "You already sent them a friend request.")
                    print("You already sent them a friend request.")
                    return redirect(previous_path)
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                messages.success(request, "Friend request sent.")
                print("Friend request sent.")
        else:
            friend_request = FriendRequest(sender=user, receiver=receiver)
            friend_request.save()
            messages.success(request, "Friend request sent.")
            print("Friend request sent.")
    return redirect(previous_path)


@login_required(login_url='login-user')
def show_requests(request):
    friend_requests, search_query = profilesearch(request)
    friend_requests, custom_range = profilesPaginate(request, friend_requests, 6)
    context = {
        "friend_requests": friend_requests,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, 'friends/request.html', context)


@login_required(login_url='login-user')
def accept_friend_request(request, pk):
    previous_path = request.META.get('HTTP_REFERER')
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
    print(friend_request, pk)
    return redirect(previous_path)


@login_required(login_url='login-user')
def unfriend_user(request, pk):
    previous_path = request.META.get('HTTP_REFERER')
    user = request.user
    try:
        removee = Profile.objects.get(pk=pk)
        friend_list = FriendList.objects.get(user=user)
        try:
            friend_list.unfriend(removee.user)
            messages.success(request, "Successfully removed that friend.")
        except:
            messages.error(request, "Something went wrong.")

    except:
        messages.error(request, "Unable to remove friend.")
    return redirect(previous_path, pk=pk)


@login_required(login_url="login-user")
def decline_friend(request, pk):
    previous_path = request.META.get('HTTP_REFERER')
    try:
        friend_request = FriendRequest.objects.get(pk=pk)
        if friend_request.receiver == request.user:
            try:
                friend_request.decline()
                messages.success(request, "Friend request declined")
            except:
                messages.error(request, "Something went wrong.")
        else:
            messages.error(request, "That is not your request to decline")
    except:
        messages.error(request, "Friend request is't accessible")

    return redirect(previous_path, pk=pk)


@login_required(login_url="login-user")
def cancel_friend(request, pk):
    previous_path = request.META.get('HTTP_REFERER')
    try:
        receiver = Profile.objects.get(pk=pk).user
        try:
            friend_request = FriendRequest.objects.filter(receiver = receiver, sender = request.user, is_active = True)
            print(friend_request)
            if len(friend_request) > 1:
                for req in friend_request:
                    req.cancel()
                    req.delete()
            else:
                friend_request.first().cancel()
                friend_request.first().delete()
            messages.success(request, "Friend request is canceled")
        except:
            messages.error(request, "Friend request is't accessible.")
    except:
        messages.error(request, "Unable to cancel friend request.")
    return redirect(previous_path, pk=pk)


def friend_list(request, user_id):
    profile  = Profile.objects.get(pk=user_id)
    friend_for_user =  FriendList.objects.get(user=request.user).friends.all()
    friends, user_friends, search_query, is_self, friend_request = profilesearch(request, flag=True, user_id=user_id)
    friends, custom_range = profilesPaginate(request, friends, 6)
    context = {
        'page': "friend_page",
        "friends": friends,
        "user_friends": user_friends,
        "friend_for_user": friend_for_user,
        "is_self": is_self,
        "search_query": search_query,
        "moder": profile.user,
        "custom_range": custom_range,
        # "is_friend": is_friend,
        "friend_request": friend_request
    }
    print(context)
    # , is_friend, request_sent

    return render(request, 'friends/friends.html', context) 