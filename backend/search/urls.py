from django.urls import path
from .api import *


urlpatterns = [
    path('', search,name='search')
]
