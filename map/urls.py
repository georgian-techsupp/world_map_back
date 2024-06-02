from .views import  fetch_business_locations
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)


urlpatterns = [
    path('fetch-locations/', fetch_business_locations, name='fetch-locations'),
    path('', include(router.urls)),
]
