import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Country
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Country
from .serializers import CountrySerializer


@api_view(['GET'])
def fetch_business_locations(request):
    iso_code = request.query_params.get('iso_code')
    if not iso_code:
        return Response({'error': 'ISO code is required'}, status=400)

    try:
        country = Country.objects.get(iso_code=iso_code)
    except Country.DoesNotExist:
        return Response({'error': 'Country not found'}, status=404)

    google_api_key = settings.GOOGLE_API_KEY
    google_places_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

    params = {
        'query': country.business_name,
        'region': iso_code,
        'key': google_api_key,
        'type': 'restaurant'
    }

    response = requests.get(google_places_url, params=params)
    data = response.json()

    if data.get('status') != 'OK':
        return Response({'error': 'Error fetching data from Google Places API'}, status=500)

    locations = [
        {
            'name': result['name'],
            'latitude': result['geometry']['location']['lat'],
            'longitude': result['geometry']['location']['lng'],
        }
        for result in data.get('results', [])
    ]

    return Response({
        'image_url': country.image.url,
        'locations': locations
    })






class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {country.iso_code: country.image.url for country in queryset}
        return Response(data)
