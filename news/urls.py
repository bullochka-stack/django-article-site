from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/add-news', add_news, name='add_news'),
    path('news/<int:pk>', show_news, name='show_news'),
    path('login/', user_login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', user_logout, name='user_logout'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/news/edit/<int:pk>/', edit_news, name='edit_news'),
    path('profile/news/delete/<int:pk>/', delete_news, name='delete_news')
]