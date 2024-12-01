from django.urls import path
from . import views

urlpatterns = [
    path('', views.region_weather_page, name='region_weather_page'),
    path('get_weather_data/', views.get_weather_data, name='get_weather_data'),
    path('get_course_data/', views.get_course_data, name='get_course_data'),  # 코스 정보
    path('get_course_spots/', views.get_course_spots, name='get_course_spots'),  # Spot 상세 정보
]


