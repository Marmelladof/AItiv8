from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view

from web_api.serializers import CropSerializer
from web_api.models import Crop

from ml_section.model_run.run_model import main, run_model1

# Create your views here.

@api_view(["GET", "POST"])
def ideal_crop(request):
   
   if request.method == 'GET':
      crop_info = Crop.objects.all()
      serializer = CropSerializer(crop_info, many=True)
      return JsonResponse(serializer.data, safe=False)

   if request.method == 'POST':
      data = request.data
      serializer = CropSerializer(data=data)
      if serializer.is_valid():
         serializer.save()
         crop_type = run_model1(list(data.values()))
         return Response(crop_type, status=status.HTTP_201_CREATED)
