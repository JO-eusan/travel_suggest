from django.shortcuts import render
from django.http import JsonResponse
from .models import Region, Weather, Spot
from datetime import datetime, timedelta
from django.db.models import Count, Sum

def region_weather_page(request):
    """지역 선택과 날씨 데이터를 한 페이지에서 처리하는 뷰"""
    regions = Region.objects.all()
    return render(request, 'region_weather_page.html', {'regions': regions})

def get_weather_data(request):
    """선택된 지역의 날씨 데이터를 반환하는 Ajax 뷰"""
    region_id = request.GET.get('region_id')  # Ajax로 전달받은 지역 ID
    today = datetime.now()
    dates = [today + timedelta(days=i) for i in range(3)]
    date_measure_list = [int(date.strftime("%m%d")) for date in dates]

    weather_data = Weather.objects.filter(region_id=region_id, date_measure__in=date_measure_list).order_by('date_measure')

    # 날씨 데이터를 JSON 형태로 반환
    data = [
        {
            'date': w.date_measure,
            'max_temperature': w.max_temperature,
            'min_temperature': w.min_temperature,
            'precipitation': w.precipitation,
            'avg_humidity': w.avg_humidity,
        }
        for w in weather_data
    ]
    return JsonResponse({'weather_data': data})

def get_course_data(request):
    """선택된 지역의 코스 정보를 반환하는 Ajax 뷰"""
    region_id = request.GET.get('region_id')  # 지역 ID
    courses = Spot.objects.filter(region_id=region_id).values(
        'course__course_name',  # 코스 이름
        'course__course_id'     # 코스 ID
    ).annotate(
        spot_count=Count('spot_id'),        # 코스에 포함된 Spot 수
        total_time=Sum('time_move')        # 코스의 총 이동 시간
    )

    # 데이터를 JSON으로 반환
    data = [
        {
            'course_name': course['course__course_name'],
            'course_id': course['course__course_id'],
            'spot_count': course['spot_count'],
            'total_time': course['total_time']
        }
        for course in courses
    ]
    return JsonResponse({'course_data': data})


def get_course_spots(request):
    """선택된 코스에 포함된 Spot 정보를 반환하는 Ajax 뷰"""
    course_id = request.GET.get('course_id')  # 코스 ID
    spots = Spot.objects.filter(course_id=course_id).select_related('region', 'course').order_by('course_seq')

    # Spot 정보를 JSON으로 반환
    data = [
        {
            'course_seq': spot.course_seq,  # 순서
            'spot_name': spot.spot_name,  # 관광지명
            'region_name': spot.region.region_name,  # 지역명
            'course_name': spot.course.course_name,  # 테마명
            'div_inout': spot.div_inout,  # 실내구분
            'time_move': spot.time_move  # 이동 시간
        }
        for spot in spots
    ]
    return JsonResponse({'spot_data': data})
