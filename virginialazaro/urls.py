from django.contrib import admin
from django.urls import path

from vlapi.views import CategoriesViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', CategoriesViewSet.as_view({'get': 'list'})),
    path('categories/<str:name>/', CategoriesViewSet.as_view({'get': 'get'}))
]
