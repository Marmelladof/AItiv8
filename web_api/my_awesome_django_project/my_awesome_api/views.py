from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view

from my_awesome_api.serializers import CropSerializer
from my_awesome_api.models import Crop

# Create your views here.

class CropViewSet(viewsets.ModelViewSet):
   queryset = Crop.objects.all()
   serializer_class = CropSerializer

@api_view(["POST"])
def get_ideal_crop(request, *args, **kwargs):
   print(request)
   from ml_section.model_run.__main__ import main
   return 0
   # print(data)
   # crop_type = main(list(data.values()))
   # return crop_type

