from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.loginUser, name="login-user"),
    path("logout/", views.logoutUser, name="logout-user"),
    path("register/", views.registerUser, name="register-user"),
    path("", views.showprofiles, name="show-users"),
    path("moders/<str:pk>", views.profile, name="current-profile"),
    path("account/", views.userAccount, name="user-account"),
    path("edit-account/", views.editAccount, name="edit-account"),
    path("delete-account/", views.deleteAcc, name="delete-account"),
    path("add-skill/", views.createSkill, name="add-skill"),
    path("update-skill/<str:pk>", views.updateSkill, name="update-skill"),
    path("delete-skill/<str:pk>", views.deleteSkill, name="delete-skill"),
    path("inbox/", views.inbox, name="inbox"),
    path("message/<str:pk>", views.inboxMassage, name="selected-message"),
    path("send-message/<str:pk>", views.sendMessage, name="send-message"),
]
