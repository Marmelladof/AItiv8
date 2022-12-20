from rest_framework import serializers

from web_api.models import Crop

class CropSerializer(serializers.ModelSerializer):
   class Meta:
       model = Crop
       fields = ('N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall')
