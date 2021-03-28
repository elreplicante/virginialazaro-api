from django.contrib import admin
from django.urls import path

from vlapi.views import ArticlesView, CategoriesViewSet, HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', CategoriesViewSet.as_view({'get': 'list'})),
    path('categories/<str:name>/', CategoriesViewSet.as_view({'get': 'get'})),
    path('articles/', ArticlesView.as_view()),
    path('health/', HealthCheckView.as_view())
]
