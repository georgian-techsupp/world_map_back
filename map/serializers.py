from rest_framework import serializers
from .models import Country, Coordinates
from .models import ISO_CODES





class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'iso_code', 'image', 'business_name','business_type', 'Customer_website']



class Coordinates(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'