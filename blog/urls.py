from django.urls import path
from .views import RegisterView, LoginView, LogoutView  # Add this line
from . import views

urlpatterns = [
    #Authentication Urls
    path('register/', RegisterView.as_view(), name='register-page'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('logout/', LogoutView.as_view(), name='logout-page'),

    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/like/', views.like_blog, name='like_blog'),
    path('blog/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
]
