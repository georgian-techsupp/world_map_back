from rest_framework import serializers
from .models import Country, Coordinates
from .models import ISO_CODES




class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'iso_code', 'image', 'business_name','business_type',
                   'Customer_website', "costumer_fb_link" , "costumer_inst_link","costumer_x_link" ,
                   "costumer_linkedin_link"]



class Coordinates(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'