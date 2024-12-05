from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from datetime import datetime, timedelta

def execute_sql(query, params=None):
    """SQL Query 실행 함수"""
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def region_weather_page(request):
    """지역 선택과 날씨 데이터를 한 페이지에서 처리하는 뷰"""
    regions = execute_sql("SELECT region_id, region_name FROM travel_region")
    return render(request, 'region_weather_page.html', {'regions': regions})

def get_weather_data(request):
    """선택된 지역의 날씨 데이터를 반환하는 Ajax 뷰"""
    region_id = request.GET.get('region_id')
    today = datetime.now()
    dates = [today + timedelta(days=i) for i in range(3)]
    date_measure_list = [int(date.strftime("%m%d")) for date in dates]

    query = """
        SELECT 
            date_measure, 
            max_temperature, 
            min_temperature, 
            precipitation, 
            avg_humidity 
        FROM travel_weather
        WHERE region_id = %s AND date_measure IN %s
        ORDER BY date_measure
    """
    data = execute_sql(query, [region_id, tuple(date_measure_list)])
    return JsonResponse({'weather_data': data})

def get_course_data(request):
    """선택된 지역의 코스 정보를 반환하는 Ajax 뷰"""
    region_id = request.GET.get('region_id')
    query = """
        SELECT 
            c.course_id, 
            c.course_name, 
            (SELECT COUNT(*) 
            FROM travel_spot s2 
            WHERE s2.course_id = c.course_id) AS spot_count, 
            (SELECT s2.time_move * 10
             FROM travel_spot s2
             WHERE s2.course_id = c.course_id
             ORDER BY s2.course_seq DESC
             LIMIT 1) AS total_time
        FROM travel_course c
        WHERE EXISTS (SELECT 1 FROM travel_spot s WHERE s.course_id = c.course_id AND s.region_id = %s)
    """
    data = execute_sql(query, [region_id])
    return JsonResponse({'course_data': data})

def get_course_spots(request):
    """선택된 코스에 포함된 Spot 정보를 반환하는 Ajax 뷰"""
    course_id = request.GET.get('course_id')
    query = """
        SELECT 
            s.course_seq, 
            s.spot_name, 
            r.region_name, 
            c.course_name, 
            s.div_inout, 
            COALESCE(s.time_move - LAG(s.time_move, 1) OVER (PARTITION BY s.course_id ORDER BY s.course_seq), 0) * 10 AS actual_time
        FROM travel_spot s
        JOIN travel_region r ON s.region_id = r.region_id
        JOIN travel_course c ON s.course_id = c.course_id
        WHERE s.course_id = %s
        ORDER BY s.course_seq
    """
    data = execute_sql(query, [course_id])
    return JsonResponse({'spot_data': data})
