from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<entry_name>', views.entry_page, name='entry_page'),
    path('search/', views.search, name='search'),
    path('random_page/', views.random_page, name='random_page'),
    path('new_page/', views.new_page, name='new_page'),
    path('edit_page/<entry_name>', views.edit_page, name='edit_page'),
]
