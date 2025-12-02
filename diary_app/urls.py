from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='diary_app/login.html'
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('set-pin/', views.set_pin_view, name='set_pin'),
    path('unlock/', views.unlock_diary_view, name='unlock_diary'),

    path('', views.diary_home_view, name='diary_home'),
    path('new/', views.diary_new_view, name='diary_new'),
    path('entry/<int:pk>/', views.diary_detail_view, name='diary_detail'),
]
