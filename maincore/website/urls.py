from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import HomeListView, HomeDetailView, AdvertCreateView, AdvertUpdateView, AdvertDeleteView, profile_view, update_comment_status, ConfirmUser, account_inactive

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('detail/<int:pk>', HomeDetailView.as_view(), name='detail_page'),
    path('edit-page', AdvertCreateView.as_view(), name='edit_page'),
    path('update_page/<int:pk>', AdvertUpdateView.as_view(), name='update_page'),
    path('delete_page/<int:pk>', AdvertDeleteView.as_view(), name='delete_page'),
    path('profile/', profile_view, name='profile'),
    #path('signup/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'),
         name='logout'),
    path('inactive/', account_inactive, name="account_inactive"),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),

    #ajax
    path('update_comment_status/<int:pk>/<slug:type>', update_comment_status, name='update_comment_status')
]