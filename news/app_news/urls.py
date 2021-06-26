from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.AnotherLoginView.as_view(), name='login'),
    path('logout/', views.AnotherLogoutView.as_view(), name='logout'),
    path('news_list/', views.NewsView.as_view(), name='news'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('create_new_news/', views.CreateNews.as_view(), name='create_new_news'),
    path('news/<int:news_id>/news_edit/', views.NewsEdit.as_view(), name='news_edit'),
    path('register/', views.register_view, name='register'),
    path('account/', views.account_view, name='account'),
    path('unpublished_news/', views.UnpublishedNews.as_view(), name='unpublished_news'),
    path('unverified_users/', views.UnverifiedUsers.as_view(), name='unverified_users'),
    path('news_list/<slug:tag>/', views.news_tag, name='news-tag'),
]
