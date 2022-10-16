from email.mime import image
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import users

from users.views import profile
from . import utils
from .models import Mod, Gallery
from .forms import ModForm, ReviewForm


def showmods(request):
    data, search_query = utils.modSearch(request)
    mods, custom_range = utils.modPaginate(request, data, 6)

    context = {'mods':mods, 'search_query': search_query,
             'custom_range': custom_range
    }
    return render(request, 'projects/modpage.html', context)


def currentmod(request, pk):
    data = Mod.objects.get(id=pk)
    print(pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.mod = data
        review.owner = request.user.profile
        review.save()

        messages.success(request, "U'r review was successfully submitted")
        return redirect('modpage', pk=data.id)
    
    if data.getVoteCount:
        data.getVoteCount
    context = {'mod': data, 'form':form}
    return render(request, 'projects/currentmod.html', context)


@login_required(login_url='login-user')
def createMod(request):
    profile = request.user.profile
    
    forms = ModForm()
    if request.method == 'POST':
        print(request.POST)
        forms = ModForm(request.POST, request.FILES)
        if forms.is_valid():
            mod = forms.save(commit=False)
            mod.owner = profile
            mod.save()
            return redirect('home')
    

             
    context = {'forms': forms}
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login-user')
def updateMod(request, pk):
    profile = request.user.profile
    mod = profile.mod_set.get(id=pk)
    forms = ModForm(instance=mod)

    if request.method == 'POST':
        forms = ModForm(request.POST, request.FILES ,instance=mod)
        if forms.is_valid():
            forms.save()
            return redirect('user-account')
             
    context = {'forms': forms}
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login-user')
def deleteMod(request, pk):
    profile = request.user.profile
    mod = profile.mod_set.get(id=pk)
    if request.method == 'POST':
        mod.delete()
        return redirect('user-account')
    context = {'obj': mod}
    return render(request, 'delete.html', context)


def modGallery(request, pk):
    mod = Mod.objects.get(id=pk)
    images = mod.gallery_set.all()
    author_images = images.filter(user_owner=mod.owner)
    users_images = []
    for image in images:
        if image not in author_images:
            users_images.append(image)
    context = {'mod':mod, 'images': images,
      'Author': author_images, 'Users':users_images}
    return render(request, 'projects/gallery.html', context)


@login_required(login_url='login-user')
def addImage(request, pk):
    mod = Mod.objects.get(id=pk)
    print(mod)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for i in images:
            item = Gallery.objects.create(
                parent = mod,
                user_owner = request.user.profile,
                img = i
            )
            item.save()
        return redirect('edit-gallery', pk=pk)
    context = {'page':'addimage'}
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login-user')
def editGallery(request, pk):
    profile = request.user.profile
    mod = Mod.objects.get(id=pk)
    images = mod.gallery_set.all().filter(
        user_owner = profile.id
    )
    context = {'page':'page', 'images':images, 'mod':mod}
    return render(request, 'projects/gallery.html', context)


@login_required(login_url='login-user')
def deleteImg(request, pk):
    img = Gallery.objects.get(id=pk)
    mod = img.parent.id
    if request.method == 'POST':
        img.delete()
        return redirect('edit-gallery', pk=mod)
    context = {'obj': img}
    return render(request, 'delete.html', context)