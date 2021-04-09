
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),

    path('countries/', views.CountryList.as_view(), name=views.CountryList.name),
    path('countries/<int:pk>', views.CountryDetail.as_view(), name=views.CountryDetail.name),
    path('countries/<int:pk>/regions', views.country_regions, name='country-region-list'),
    path('countries/<int:pk>/producers', views.country_producers, name='country-producer-list'),
    path('countries/<int:pk>/wines', views.country_wines, name='country-wine-list'),
    path('countries/<int:pk>/grapes', views.country_grapes, name='country-grape-list'),

    path('regions/', views.RegionList.as_view(), name=views.RegionList.name),
    path('regions/<int:pk>', views.RegionDetail.as_view(), name=views.RegionDetail.name),
    path('regions/<int:pk>/wines', views.region_wines, name='region-wine-list'),
    path('regions/<int:pk>/producers', views.region_producers, name='region-producer-list'),
    path('regions/<int:pk>/grapes', views.region_grapes, name='region-grape-list'),

    path('producer-regions/', views.ProducerRegionList.as_view(), name=views.ProducerRegionList.name),
    path('producer-regions/<int:pk>', views.ProducerRegionDetail.as_view(), name=views.ProducerRegionDetail.name),

    path('producers/', views.ProducerList.as_view(), name=views.ProducerList.name),
    path('producers/<int:pk>', views.ProducerDetail.as_view(), name=views.ProducerDetail.name),
    path('producers/<int:pk>/wines', views.producer_wines, name='producer-wine-list'),
    path('producers/<int:pk>/vintages', views.producer_vintages, name='producer-vintage-list'),

    # path('grape-types/', views.grape_type_list.as_view(), name='grape-type-list'),
    # path('grape-types/<str:type>', views.grape_type_detail.as_view(), name='grape-type-detail'),
    # path('grape-types/<str:type>/grapes', views.grape_type_grapes_list.as_view(), name='grape-type-grape-list'),

    # path('wine-types/', views.wine_type_list.as_view(), name='wine-type-list'),
    # path('wine-types/<str:type>', views.wine_type_detail.as_view(), name='wine-type-detail'),
    # path('wine-types/<str:type>/wines', views.wine_type_wines_list.as_view(), name='wine-type-wine-list'),

    path('grapes/', views.GrapeList.as_view(), name=views.GrapeList.name),
    path('grapes/<int:pk>', views.GrapeDetail.as_view(), name=views.GrapeDetail.name),
    path('grapes/<int:pk>/wines', views.grape_wines, name='grape-wine-list'),

    path('wine-grapes/', views.WineGrapeList.as_view(), name=views.WineGrapeList.name),
    path('wine-grapes/<int:pk>', views.WineGrapeDetail.as_view(), name=views.WineGrapeDetail.name),

    path('wines/', views.WineList.as_view(), name=views.WineList.name),
    path('wines/<int:pk>', views.WineDetail.as_view(), name=views.WineDetail.name),
    path('wines/<int:pk>/vintages', views.wine_vintages, name='wine-vintage-list'),
    path('wines/<int:pk>/reviews', views.wine_reviews, name='wine-review-list'),

    path('vintages/', views.VintageList.as_view(), name=views.VintageList.name),
    path('vintages/<int:pk>', views.VintageDetail.as_view(), name=views.VintageDetail.name),
    path('vintages/<int:pk>/reviews', views.vintage_reviews, name='vintage-review-list'),

    path('grape-aliases/', views.GrapeAliasList.as_view(), name=views.GrapeAliasList.name),
    path('grape-aliases/<int:pk>', views.GrapeAliasDetail.as_view(), name=views.GrapeAliasDetail.name),

    # does it make sense to be able to access every single review like this?
    path('reviews/', views.ReviewList.as_view(), name=views.ReviewList.name),
    path('reviews/<int:pk>', views.ReviewDetail.as_view(), name=views.ReviewDetail.name),

    # how to name these correctly according to the conventions?
    # path('year/vintages/', ...),
    # path('year/<int:year>/vintages/', ...),
    # path('vintages/year/', views.vintages_per_year_list.as_view(), name='vintages-per-year-list'),
    # path('vintages/year/<int:pk>', views.vintages_per_year_detail.as_view(), name='vintages-per-year-detail'),
    # path('user/reviews/', ...),
    # path('user/<int:pk>/reviews/', ...),
    # path('reviews/user/', views.ReviewList.as_view(), name=views.ReviewList.name),
    # path('reviews/user/<int:pk>', views.ReviewList.as_view(), name=views.ReviewList.name),
]

