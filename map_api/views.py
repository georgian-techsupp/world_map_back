from django.shortcuts import render
from rest_framework import viewsets
from .models import World_Map_Model
from .serializers import Wordls_Map_Serializer
from .permissions import isSuperUserOrReadOnly

# Create your views here.

class Wordl_Map_View(viewsets.ModelViewSet):
    queryset = World_Map_Model.objects.all()
    serializer_class = Wordls_Map_Serializer
    permission_classes = [isSuperUserOrReadOnly]
