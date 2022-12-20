from django.urls import include, path

from rest_framework import routers

from web_api.views import ideal_crop

router = routers.DefaultRouter()

urlpatterns = [
   path('', include(router.urls)),
   path('crop_type', ideal_crop)
]