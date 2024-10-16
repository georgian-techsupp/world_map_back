from .views import  fetch_business_locations, get_google_points
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet , get_google_points_for_countries

router = DefaultRouter()
router.register(r'countries', CountryViewSet)


urlpatterns = [
    path('fetch-locations/', fetch_business_locations, name='fetch-locations'),
    path('', include(router.urls)),
    path('test/',get_google_points, name = "test"),
    path('admin/get-google-points/<str:iso_codes>/', get_google_points_for_countries, name='admin_get_google_points'),
]
