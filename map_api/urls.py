from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Wordl_Map_View
router = DefaultRouter()
router.register(r"map", Wordl_Map_View)

urlpatterns = [
    path('', include(router.urls))
]
