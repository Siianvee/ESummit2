from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('already-registered/', views.already_registered, name='already_registered'),
    path('fetch_ticket/', views.fetch_ticket, name='fetch_ticket'),
]
