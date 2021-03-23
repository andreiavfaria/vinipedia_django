"""vinipedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views

app_name = "wines"

urlpatterns = [
    path('wines/', views.wine_list, name='wine_list'),
    path('wines/<int:id>', views.wine_detail, name='wine_detail'),
    path('grapes/', views.grape_list, name='grape_list'),
    path('grapes/<int:id>', views.grape_detail, name='grape_detail'),
    # path('grapes/<str:type>', views.grapes_per_type, name='grapes_per_type'),
    path('producers/', views.producer_list, name='producer_list'),
    path('producers/<int:id>', views.producer_detail, name='producer_detail'),
    path('regions/', views.region_list, name='region_list'),
    path('regions/<int:id>', views.region_detail, name='region_detail'),
    # producers per region
    # wines per region
    # wines/vintages per year
    path('year/<int:year>', views.vintages_per_year, name='vintages_per_year'),
    # wine search
    path('wines/search/', views.wine_search, name='wine_search'),
    # grape search (including alias)
    path('grapes/search/', views.grape_search, name='grape_search'),
    # producer search
    path('producers/search/', views.producer_search, name='producer_search'),

    # vintages: provisional
    path('vintages/', views.vintage_list, name='vintage_list'),
    path('vintages/<int:id>', views.vintage_detail, name='vintage_detail'),
    #

]
