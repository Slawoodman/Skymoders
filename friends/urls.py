from django.urls import path
from . import views


app_name = "friends"
urlpatterns = [
    path('friend/<str:pk>', views.friendspage, name='friendlist'),
    path('friend_request/<str:pk>', views.send_friend_request, name='send_request'),
    path('requests/', views.show_requests, name="show_requests"),
    path('accept_friend/<str:pk>', views.accept_friend_request, name="accept-friend"),
    path('decline_friend/<str:pk>', views.decline_friend, name="decline-friend"),
    path('unfriend/<str:pk>', views.unfriend_user, name="unfriend"),
    path('cancel_friend/<str:pk>', views.cancel_friend, name='cancel_friend'),
    path('friendlist/<str:user_id>', views.friend_list, name='list_of_friends')
]