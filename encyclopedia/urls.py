from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<entry_name_slug>', views.entry_page, name='entry_page'),
]
