from django.urls import path
from . import views, api_views

urlpatterns = [
    # Web views (for Django templates)
    path('', views.index, name='index'),
    path('system-check/', views.system_check, name='system_check'),
    path('farm/create/', views.create_farm, name='create_farm'),
    path('farm/<int:farm_id>/', views.farm_dashboard, name='farm_dashboard'),
    path('farm/<int:farm_id>/calendar/', views.weather_calendar, name='weather_calendar'),
    path('farm/<int:farm_id>/edit/', views.edit_farm, name='edit_farm'),
    path('farm/<int:farm_id>/delete/', views.delete_farm, name='delete_farm'),
    
    # API endpoints (for React frontend)
    path('api/farms/', api_views.get_farms, name='api_farms'),
    path('api/farms/<int:farm_id>/', api_views.delete_farm, name='api_delete_farm'),
    path('api/farms/<int:farm_id>/weather/', api_views.get_farm_weather, name='api_farm_weather'),
    path('api/crops/', api_views.get_crops, name='api_crops'),
    path('api/predict/', api_views.predict_blight, name='api_predict'),
]
