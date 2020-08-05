from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<entry_name>', views.entry_page, name='entry_page'),
    path('search/', views.search, name='search'),
]
