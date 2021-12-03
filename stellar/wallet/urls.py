from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wallet/', views.wallet, name='wallet'),
    path('create', views.create, name='create'),
    path('account', views.account, name='account'),
    path('activate', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
]