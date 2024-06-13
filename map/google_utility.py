import requests
from rest_framework.response import Response
from .models import Country, ISO_CODES
from django.conf import settings

# def google_locations(request):
#     iso_code = request.query_params.get('iso_code')
#     if not iso_code:
#         return Response({'error': 'ISO code is required'}, status=400)

#     try:
#         country = ISO_CODES.objects.get(iso_code=iso_code)
#         country_name = Country.objects.get(name =country )
#     except ISO_CODES.DoesNotExist:
#         return Response({'error': 'Country not found'}, status=404)

#     google_api_key = settings.GOOGLE_API_KEY
#     google_places_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

#     params = {
#         'query': country_name.business_name,
#         'region': iso_code,
#         'key': google_api_key,
#         'type': country_name.business_type,
#     }

#     response = requests.get(google_places_url, params=params)
#     data = response.json()

#     if data.get('status') != 'OK':
#         return Response({'error': 'Error fetching data from Google Places API'}, status=500)

#     locations = [
#         {
#             'name': result['name'],
#             'latitude': result['geometry']['location']['lat'],
#             'longitude': result['geometry']['location']['lng'],
#         }
#         for result in data.get('results', [])
#     ]

#     return {
#         'image_url': country_name.image.url,
#         'locations': locations
#     }



def google_locations(query, region, bussiness_type):
    google_api_key = settings.GOOGLE_API_KEY
    google_places_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

    params = {
        'query': query,
        'region': region,
        'key': google_api_key,
        'type': bussiness_type,
    }

    response = requests.get(google_places_url, params=params)
    data = response.json()

    if data.get('status') != 'OK':
        return Response({'error': 'Error fetching data from Google Places API'}, status=500)

    locations = [
        {
            'name': result['name'],
            'latitude': float(f"{result['geometry']['location']['lat']:.6f}"),
            'longitude': float(f"{result['geometry']['location']['lng']:.6f}"),
        }
        for result in data.get('results', [])
    ]
    return {
        'locations': locations
    }
