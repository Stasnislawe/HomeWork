from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostSearch, PostCreate, IndexView, NewsDelete, NewsEdit, ArticleDelete, subscribe, ArticleEdit, CategoryListView


urlpatterns = [
   path('', PostsList.as_view(), name='news_list'),
   path('index/', IndexView.as_view(), name='index'),
   path('<int:pk>', PostDetail.as_view(), name='news_detail'),
   path('search/', PostSearch.as_view(), name='news_search'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name ='news_delete'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('article/create/', PostCreate.as_view(), name='article_create'),
   path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/sub', subscribe, name='subscribe'),
]