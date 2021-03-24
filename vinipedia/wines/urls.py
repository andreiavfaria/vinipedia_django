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
    # landing page
    path('', views.landing_page, name='landing_page'),
    # wines
    path('wines/', views.wine_list, name='wine_list'),
    path('wines/<int:id>', views.wine_detail, name='wine_detail'),
    path('wines/<str:type>', views.wines_per_type, name='wines_per_type'),
    # grapes
    path('grapes/', views.grape_list, name='grape_list'),
    path('grapes/<int:id>', views.grape_detail, name='grape_detail'),
    path('grapes/<str:type>', views.grapes_per_type, name='grapes_per_type'),
    # producers
    path('producers/', views.producer_list, name='producer_list'),
    path('producers/<int:id>', views.producer_detail, name='producer_detail'),
    # regions
    path('regions/', views.region_list, name='region_list'),
    path('regions/<int:id>', views.region_detail, name='region_detail'),
    # producers per region
    path('regions/<int:id>/producers', views.producers_per_region, name='producers_per_region'),
    # wines per region
    path('regions/<int:id>/wines', views.wines_per_region, name='wines_per_region'),
    # wines/vintages per year
    path('year/<int:year>', views.vintages_per_year, name='vintages_per_year'),
    # search
    path('search/', views.sitewide_search, name='sitewide_search'),
    path('wines/search/', views.wine_search, name='wine_search'),
    path('grapes/search/', views.grape_search, name='grape_search'),
    path('producers/search/', views.producer_search, name='producer_search'),

    # vintages: provisional
    path('vintages/', views.vintage_list, name='vintage_list'),
    path('vintages/<int:id>', views.vintage_detail, name='vintage_detail'),
    #

]
