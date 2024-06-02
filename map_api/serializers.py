from rest_framework import serializers
from .models import World_Map_Model

class Wordls_Map_Serializer(serializers.ModelSerializer):
    class Meta:
        model = World_Map_Model
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'logo' in validated_data:
            if instance.logo:
                instance.logo.delete(save=False)
            instance.logo = validated_data.get('logo', instance.logo)
        instance.country_name = validated_data.get('country_name', instance.country_name)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.save()
        return instance