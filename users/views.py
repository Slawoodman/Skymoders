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


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if "download" in request.GET["next"]:
                resolver_match = resolve(request.GET["next"])
                return redirect("modpage", pk=resolver_match.kwargs["pk"])
            return redirect(
                request.GET["next"] if "next" in request.GET else "user-account"
            )

        else:
            messages.error(request, "Username OR password is incorrect")
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


def profile(request, pk):
    moder = Profile.objects.get(id=pk)
    specSkill = moder.skill_set.exclude(description__exact="")
    addSkill = moder.skill_set.filter(description="")
    print(addSkill, specSkill)
    context = {"moder": moder, "specSkill": specSkill, "addskills": addSkill}
    return render(request, "users/profile.html", context)


@login_required(login_url="login-user")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    mods = profile.mod_set.all()
    context = {"profile": profile, "skills": skills, "mods": mods}
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
