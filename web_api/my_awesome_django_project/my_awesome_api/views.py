from django.shortcuts import render
from rest_framework import viewsets

from my_awesome_api.serializers import CropSerializer
from my_awesome_api.models import Crop

# Create your views here.

class CropViewSet(viewsets.ModelViewSet):
   queryset = Crop.objects.all()
   serializer_class = CropSerializer
