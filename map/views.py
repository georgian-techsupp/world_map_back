import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Country
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Country, Coordinates, ISO_CODES
from .serializers import CountrySerializer
from .google_utility import google_locations
import json
from decimal import Decimal, InvalidOperation
from django.shortcuts import redirect
from django.http import HttpResponse
from .permissions import IsAdminUser


@api_view(['GET'])
def fetch_business_locations(request):
    iso_code = request.query_params.get('iso_code')
    if not iso_code:
        return Response({'error': 'ISO code is required'}, status=400)
    try:
        code = ISO_CODES.objects.get(iso_code=iso_code)
        country = Country.objects.get(iso_code=code)
        locations = Coordinates.objects.filter(name=country, activate=True)
        image_url = request.build_absolute_uri(country.image.url)
    except Country.DoesNotExist:
        return Response({'error': 'Country not found'}, status=404)

    locations_data = [
        {
            'location_name': loc.location_name,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'activate': loc.activate
        }
        for loc in locations
    ]
    return Response({
        # 'image_url': image_url,
        'locations': locations_data
    })




class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {
            country.iso_code.iso_code : {
                'image_url': country.image.url,
                'customer_website': country.Customer_website,
                 "costumer_fb_link" : country.costumer_fb_link,
                 "costumer_inst_link" : country.costumer_inst_link,
                 "costumer_x_link" : country.costumer_x_link,
                 "costumer_linkedin_link" : country.costumer_linkedin_link,

            }
            for country in queryset
        }
        return Response(data)


@api_view(['GET'])
def get_google_points(request):
    """gets locations depend on bussines names, 
    splits it and adding data in db for each bussiness name"""
    try:
        iso_code = request.query_params.get('iso_code')
        if not iso_code:
            return Response({'error': 'not provided query parameter iso_code'}, status=400)
        country = ISO_CODES.objects.get(iso_code=iso_code)
        country_name = Country.objects.get(name=country)
        business_names = []
        if "," in country_name.business_name:
            b_names = country_name.business_name.split(",")
            for item in b_names:
                business_names.append(item.strip())
        else:
            business_names.append(country_name.business_name)
        for business in business_names:
            data = google_locations(business, country.iso_code, country_name.business_type)
            for location in data['locations']:
                try:
                    latitude = float(f"{Decimal(location['latitude']):.6f}")
                    longitude = float(f"{Decimal(location['longitude']):.6f}")
                    _, created = Coordinates.objects.get_or_create(
                        name=country_name,
                        iso_code=country_name,
                        business_name=country_name,
                        location_name=location['name'],
                        latitude=latitude,
                        longitude=longitude,
                    )
                    if not created:
                        print(f"Coordinate with latitude {latitude} and longitude {longitude} already exists.")
                except InvalidOperation:
                    continue
    except ISO_CODES.DoesNotExist:
        return Response({'error': 'ISO code does not exist'}, status=400)
    except Country.DoesNotExist:
        return Response({'error': 'Country does not exist at this moment'}, status=400)
    return Response({'success': f'added locations for {iso_code}'})




def get_google_points_for_countries(request, iso_codes):
    iso_code_list = iso_codes.split(',')
    for iso_code in iso_code_list:
        try:
            country = ISO_CODES.objects.get(iso_code=iso_code)
            country_name = Country.objects.get(iso_code=country)
            business_names = []
            if "," in country_name.business_name:
                b_names = country_name.business_name.split(",")
                for item in b_names:
                    business_names.append(item.strip())
            else:
                business_names.append(country_name.business_name)
            for business in business_names:
                data = google_locations(business, country.iso_code, country_name.business_type)
                for location in data['locations']:
                    try:
                        latitude = float(f"{Decimal(location['latitude']):.6f}")
                        longitude = float(f"{Decimal(location['longitude']):.6f}")
                        _, created = Coordinates.objects.get_or_create(
                            name=country_name,
                            iso_code=country_name,
                            business_name=country_name,
                            location_name=location['name'],
                            latitude=latitude,
                            longitude=longitude,
                        )
                        if not created:
                            print(f"Coordinate with latitude {latitude} and longitude {longitude} already exists.")
                    except InvalidOperation:
                        continue
        except ISO_CODES.DoesNotExist:
            return HttpResponse(f'ISO code {iso_code} does not exist', status=400)
        except Country.DoesNotExist:
            return HttpResponse(f'Country with ISO code {iso_code} does not exist at this moment', status=400)
    return redirect('/admin/map/country/')



def health_check(request):
    return HttpResponse("OK")