from rest_framework import serializers

from my_awesome_api.models import Crop

class CropSerializer(serializers.ModelSerializer):
   class Meta:
       model = Crop
       fields = ('N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label')
