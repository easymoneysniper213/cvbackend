from django.urls import path
from api.views import search_view

urlpatterns = [
    path('api/search/', search_view, name='search'),
]
