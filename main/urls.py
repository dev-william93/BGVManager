from django.urls import path
from . views import *

urlpatterns = [
    path('media/uploads/<str:file>', secureView, name='secure')
]