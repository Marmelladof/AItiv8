from django.urls import include, path

from rest_framework import routers

from my_awesome_api.views import CropViewSet

router = routers.DefaultRouter()
router.register(r'crop', CropViewSet)

urlpatterns = [
   path('', include(router.urls)),
]