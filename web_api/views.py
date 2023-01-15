from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers
from django.http import HttpResponse

from web_api.serializers import CropSerializer
from web_api.models import CropSuggestion
import json
import copy

from ml_section.model_run.run_model import run_model1
from pltn_section.plan import optimization
from utils_api.treemap import (plot_treemap,
                               plot_money_bar_chart,
                               plot_cvp_bar_chart,
                               plot_final_treemap)

# Create your views here.

@api_view(["GET", "POST"])
def ideal_crop(request):
   
   if request.method == 'GET':
      crop_info = CropSuggestion.objects.all()
      serializer = CropSerializer(crop_info, many=True)
      return JsonResponse(serializer.data, safe=False)

   if request.method == 'POST':
      CropSuggestion.objects.all().delete()
      data = request.data
      data_values = data
      areas = []
      crop_suggestions = []
      tags = []
      counter = 0
      for soil_data in data_values:
         print(soil_data)
         areas.append(soil_data["area"])
         del soil_data["area"]

         with open("utils_api/inv_encoded_labels.json", "r") as label_file:
            labels = json.load(label_file)
         prediction = run_model1(list(soil_data.values()))
         key_list = list(prediction)
         for key in key_list:
            prediction[labels[key]] = prediction.pop(key)
         crop_suggestions.append(prediction)
         prediction["area"] = areas[-1]
         serializer = CropSerializer(data=prediction)
         if serializer.is_valid():
            serializer.save()
         else:
            print(crop_suggestions[-1])
         counter += 1
         tags.append(f"area{counter}")
      plot_treemap(crop_suggestions, areas, tags)
      image_data = open("delete.png", "rb").read()
      return HttpResponse(image_data, content_type="image/png", status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def optimized_planning(request):

   if request.method == 'POST':
      data_values = request.data
      population = data_values["population"]
      del data_values["population"]
      raw_data = serializers.serialize("json", CropSuggestion.objects.all())
      raw_data = json.loads(raw_data)
      predictions = {}
      areas = {}
      for prediction in raw_data:
         areas[prediction["pk"]] = prediction["fields"]["area"]
         del prediction["fields"]["area"]
         predictions[prediction["pk"]] = prediction["fields"]
      solution, solution_val, selected_crops, used_crops, prod, consumptions, guito_per_crop = optimization(predictions, areas, population, data_values)
      plot_money_bar_chart(selected_crops, guito_per_crop)
      plot_cvp_bar_chart(selected_crops, prod, consumptions)
      plot_final_treemap(solution, areas)
      return HttpResponse({"response": "Huge success!"}, status=status.HTTP_201_CREATED)
      
      
