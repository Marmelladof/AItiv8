from rest_framework import serializers

from web_api.models import CropSuggestion

class CropSerializer(serializers.ModelSerializer):
   class Meta:
       model = CropSuggestion
       fields = ("area", "apple", "banana", "blackgram", "chickpea", "coconut", "coffee", "cotton", "grapes", "jute", "kidneybeans", "lentil", "maize", "mango", "mothbeans", "mungbean", "muskmelon", "orange", "papaya", "pigeonpeas", "pomegranate", "rice", "watermelon")
