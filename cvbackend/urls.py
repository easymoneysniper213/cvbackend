from django.urls import path
from api.views import search_view
from api.views import details_comparison

urlpatterns = [
    path('api/search/', search_view, name='search'),
    path('api/details/', details_comparison, name='details_comparison'),
]
