from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.showmods, name='home'),
    path('mod/<str:pk>/', views.currentmod, name='modpage'),
    path('create-mod/', views.createMod, name='create-mod'),
    path('update-mod/<str:pk>/', views.updateMod, name='update-mod'),
    path('delete-mod/<str:pk>/', views.deleteMod, name='delete-mod'),
    path('gallery/<str:pk>/', views.modGallery, name='gallery'),
    path('gallery/addimages/<str:pk>', views.addImage, name='add-images'),
    path('update-gallery/<str:pk>', views.editGallery, name='edit-gallery'),
    path('gallery/delete/<str:pk>', views.deleteImg, name='delete-img'),
    path('mod/download/<str:pk>/', views.download_view, name='downloadmod')
]