import users
import os
import mimetypes
import pathlib

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.views import profile


from . import utils
from .models import Mod, Gallery
from .forms import ModForm, ReviewForm, ImageForm


def convert_bytes(size):
    """Convert bytes to KB, or MB or GB"""
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return "%3.1f%s" % (size, x)
        size /= 1024.0


def showmods(request):
    data, search_query = utils.modSearch(request)
    mods, custom_range = utils.modPaginate(request, data, 6)

    context = {"mods": mods, "search_query": search_query, "custom_range": custom_range}
    return render(request, "projects/modpage.html", context)


def currentmod(request, pk):
    data = Mod.objects.get(id=pk)
    print(pk)
    data.view_count += 1
    data.save()
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.mod = data
        review.owner = request.user.profile
        review.save()
        messages.success(request, "U'r review was successfully submitted")
        return redirect("modpage", pk=data.id)
    
    file_path = data.modfile.path
    try:
        os.path.exists(file_path)
        f_size = os.path.getsize(file_path)
        size = convert_bytes(f_size)
    except:
        size = '0.0 bytes'

            
    
    if data.getVoteCount:
        data.getVoteCount
    
    context = {"mod": data, "form": form, "size": size}
    return render(request, "projects/currentmod.html", context)


@login_required(login_url="login-user")
def createMod(request):
    profile = request.user.profile

    forms = ModForm()
    if request.method == "POST":
        print(request.POST)
        forms = ModForm(request.POST, request.FILES)
        if forms.is_valid():
            mod = forms.save(commit=False)
            mod.owner = profile
            mod.save()
            return redirect("home")

    context = {"forms": forms}
    return render(request, "projects/form-template.html", context)


@login_required(login_url="login-user")
def updateMod(request, pk):
    profile = request.user.profile
    mod = profile.mod_set.get(id=pk)
    forms = ModForm(instance=mod)

    if request.method == "POST":
        forms = ModForm(request.POST, request.FILES, instance=mod)
        if forms.is_valid():
            forms.save()
            return redirect("user-account")

    context = {"forms": forms}
    return render(request, "projects/form-template.html", context)


@login_required(login_url="login-user")
def download_view(request, pk):
    try:
        file_instance = Mod.objects.get(id=pk)
    except Mod.DoesNotExist:
        messages.error(request, "File not found.")
        return redirect("modpage", pk=file_instance.id)

    file_path = file_instance.modfile.path
    file_name = os.path.basename(file_path)
    original_extension = os.path.splitext(file_name)[1]

    # Set the content type based on the file extension
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = "application/octet-stream"

    response = HttpResponse(content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'

    try:
        with open(file_path, "rb") as f:
            response.write(f.read())

        messages.success(request, "File is successful downloaded.")
        return response

    except Exception as e:
        messages.error(request, f"File download failed: {str(e)}")
        return redirect("modpage", pk=file_instance.id)


@login_required(login_url="login-user")
def deleteMod(request, pk):
    profile = request.user.profile
    mod = profile.mod_set.get(id=pk)
    if request.method == "POST":
        mod.delete()
        return redirect("user-account")
    context = {"obj": mod}
    return render(request, "delete.html", context)


def modGallery(request, pk):
    filtro = request.GET.get('imageFilter')
    try:
        mod = Mod.objects.get(id=pk)
        images = mod.gallery_set.all()
        
        if filtro == 'mod_owner':
            images = images.filter(user_owner=mod.owner)
        elif filtro == 'users':
            images = images.exclude(user_owner=mod.owner)
    except:
        pass
    images, custom_range = utils.modPaginate(request, images, 6)
    context = {
        "mod": mod,
        "images": images,
        "custom_range": custom_range,
        "imageFilter": filtro
    }
    print(request.user, mod.owner)
    return render(request, "projects/gal.html", context)


@login_required(login_url="login-user")
def addImage(request, pk):
    mod = Mod.objects.get(id=pk)
    print(mod)
    if request.method == "POST":
        images = request.FILES.getlist("images")
        for i in images:
            item = Gallery.objects.create(
                parent=mod, user_owner=request.user.profile, img=i
            )
            item.save()
        return redirect("edit-gallery", pk=pk)
    context = {"page": "addimage"}
    return render(request, "projects/form-template.html", context)


@login_required(login_url="login-user")
def editGallery(request, pk):
    mod = Mod.objects.get(id=pk)
    filtro = ''
    if request.user == mod.owner.user:
        images = mod.gallery_set.all()
        filtro = request.GET.get('imageFilter')
        if filtro == 'mod_owner':
            images = images.filter(user_owner=mod.owner)
        elif filtro == 'users':
            images = images.exclude(user_owner=mod.owner)
        print('tyt')
    else:
        profile = request.user.profile
        images = mod.gallery_set.all().filter(user_owner=profile.id)
        print('ne tyt')

    images, custom_range = utils.modPaginate(request, images, 6)
    context = {
        "page": "page",
        "mod": mod,
        "images": images,
        "custom_range": custom_range,
        "imageFilter": filtro
    }
    return render(request, "projects/gal.html", context)

@login_required(login_url="login-user")
def change_img(request, pk):
    img = get_object_or_404(Gallery, id=pk)
    mod = img.parent.id
    if request.user == img.user_owner.user:
        form = ImageForm(instance=img)
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES, instance=img)
            if form.is_valid():
                form.save()
                return redirect("edit-gallery", pk=mod)
    else:
        messages.error(request, "U can't change another user image")
        return redirect("edit-gallery", pk=mod)
    context = {'form':form,'img': img, 'page':'change'}
    return render(request, "projects/form-template.html", context)

@login_required(login_url="login-user")
def deleteImg(request, pk):
    img = Gallery.objects.get(id=pk)
    mod = img.parent.id
    if request.method == "POST":
        img.delete()
        return redirect("edit-gallery", pk=mod)
    context = {"obj": img, 'page': 'img'}
    return render(request, "delete.html", context)
