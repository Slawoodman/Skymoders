from django.urls import resolve
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib import messages
from . import utils
from .models import Profile, Skill, Message
from friends.models import FriendList, FriendRequest
from friends.utils import get_frine_requet_or_false
from friends.fin_re import FriendRequestStatus


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist")
            return redirect("login-user")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next")
            if next_url and "download" in next_url:
                resolver_match = resolve(next_url)
                return redirect("modpage", pk=resolver_match.kwargs["pk"])
            return redirect(next_url or "user-account")

        else:
            messages.error(request, "Username or password is incorrect")
    context = {"page": page}
    return render(request, "users/login_register.html", context)


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was sucssefully created")
            login(request, user)
            return redirect("edit-account")
        else:
            messages.error(request, "An error dur registations")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "User was logged out ")
    return redirect("show-users")


def showprofiles(request):
    moders, search_query = utils.profilesearch(request)
    print(moders)
    moders, custom_range = utils.profilesPaginate(request, moders, 6)
    print(moders)
    # moders = Profile.objects.all()
    context = {
        "moders": moders,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "users/profiles.html", context)


@login_required(login_url="login-user")
def profile(request, pk):
    context = {}
    moder = Profile.objects.get(id=pk)
    specSkill = moder.skill_set.exclude(description__exact="")
    addSkill = moder.skill_set.filter(description="")
    context["addskills"] = addSkill
    context["moder"] = moder
    context["moder_id"] = moder.id
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

    fried = FriendList.objects.get(user=moder.user).friends.all()
    print(len(FriendList.objects.get(user=moder.user).friends.all()))

    context["acc_friends"] = len(fried)
    context["friends"] = friends

    if user.is_authenticated and user != moder.user:
        is_self = False
        if friends.filter(pk=moder.user.id):
            is_friend = True
        else:
            if get_frine_requet_or_false(sender=moder.user, receiver=user) != False:
                request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
            elif get_frine_requet_or_false(sender=user, receiver=moder.user) != False:
                request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
            else:
                request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

    elif not user.is_authenticated:
        is_self = False

    else:
        try:
            friend_requests = FriendRequest.objects.filter(
                receiver=moder.user, is_active=True
            )
        except:
            pass
    context["is_friend"] = is_friend
    context["is_self"] = is_self
    context["friend_requests"] = friend_requests
    context["request_sent"] = request_sent
    try:
        rqst = FriendRequest.objects.get(
            sender=moder.user, receiver=user, is_active=True
        )
        context["request_id"] = rqst.id
    except:
        pass
    print(context)
    return render(request, "users/profile.html", context)


@login_required(login_url="login-user")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    mods = profile.mod_set.all()
    requests = FriendRequest.objects.filter(receiver=profile.user, is_active=True)
    friends = len(FriendList.objects.get(user=profile.user).friends.all())
    context = {
        "profile": profile,
        "skills": skills,
        "mods": mods,
        "friend_requests": requests,
        "acc_friends": friends,
    }
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("user-account")
    context = {"form": form}
    return render(request, "users/form-template.html", context)


@login_required(login_url="login")
def deleteAcc(request):
    AccName = request.user.profile.username
    user_account = request.user.profile
    if request.method == "POST":
        user_account.delete()
        return redirect("home")
    context = {"obj": AccName, "page": "delacc"}
    return render(request, "delete.html", context)


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            messages.success(request, "Skill was successfully added")
            return redirect("user-account")

    context = {"form": form}
    return render(request, "users/form-template.html", context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()

            messages.success(request, "Skill tree was successfully updated")
            return redirect("user-account")

    context = {"form": form}
    return render(request, "users/form-template.html", context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        return redirect("user-account")

    context = {"obj": skill}
    return render(request, "delete.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messagesRequest = profile.messages.all()
    unread = messagesRequest.filter(is_read=False).count()
    сontext = {"messagesRequest": messagesRequest, "unread": unread}
    return render(request, "users/inbox.html", сontext)


@login_required(login_url="login")
def inboxMassage(request, pk):
    profile = request.user.profile
    current_message = profile.messages.get(id=pk)
    if current_message.is_read == False:
        current_message.is_read = True
        current_message.save()
    context = {"current_message": current_message}
    return render(request, "users/message.html", context)


@login_required(login_url="login")
def sendMessage(request, pk):
    receiver = Profile.objects.get(id=pk)
    form = MessageForm()
    sender = request.user.profile
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receiver = receiver
            message.email = sender.email
            message.name = sender.name
        message.save()

        messages.success(request, "U'r message was successfully sent")
        return redirect("current-profile", pk=receiver.id)

    context = {"form": form}
    return render(request, "users/form-template.html", context)
