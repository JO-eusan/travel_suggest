import csv
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Import CSV data into the database"

    def execute_sql(self, query, params=None):
        """SQL Query 실행 함수"""
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])

    def handle(self, *args, **kwargs):
        self.clear_tables()  # 기존 데이터 초기화
        self.import_courses()
        self.import_regions()
        self.import_spots()
        self.import_weather()
        self.stdout.write(self.style.SUCCESS("Successfully imported all data"))

    def clear_tables(self):
        """초기 데이터를 삭제합니다."""
        self.execute_sql("DELETE FROM travel_course")
        self.execute_sql("DELETE FROM travel_region")
        self.execute_sql("DELETE FROM travel_spot")
        self.execute_sql("DELETE FROM travel_weather")
        self.stdout.write("Cleared all tables")

    def import_courses(self):
        """Course 데이터를 CSV에서 가져옵니다."""
        with open("table/Course.CSV", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row["course_id"].strip() or not row["course_name"].strip():
                    continue
                self.execute_sql(
                    "INSERT INTO travel_course (course_id, course_name) VALUES (%s, %s)",
                    [int(row["course_id"]), row["course_name"]]
                )
        self.stdout.write("Imported Course data")

    def import_regions(self):
        """Region 데이터를 CSV에서 가져옵니다."""
        with open("table/Region.CSV", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row["region_id"].strip() or not row["region_name"].strip():
                    continue
                self.execute_sql(
                    "INSERT INTO travel_region (region_id, region_name) VALUES (%s, %s)",
                    [int(row["region_id"]), row["region_name"]]
                )
        self.stdout.write("Imported Region data")

    def import_spots(self):
        """Spot 데이터를 CSV에서 가져옵니다."""
        with open("table/Spot.CSV", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row["spot_id"].strip() or not row["spot_name"].strip():
                    continue
                self.execute_sql(
                    """
                    INSERT INTO travel_spot 
                    (spot_id, spot_name, course_id, region_id, course_seq, time_move, div_inout, tema_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        int(row["spot_id"]),
                        row["spot_name"],
                        int(row["course_id"]),
                        int(row["region_id"]),
                        int(row["course_seq"]),
                        int(row["time_move"]),
                        row["div_inout"],
                        row["tema_name"]
                    ]
                )
        self.stdout.write("Imported Spot data")

    def import_weather(self):
        """Weather 데이터를 CSV에서 가져옵니다."""
        with open("table/Weather.CSV", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.execute_sql(
                    """
                    INSERT INTO travel_weather 
                    (region_id, date_measure, avg_humidity, avg_windspeed, max_temperature, min_temperature, precipitation)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        int(row["region_id"]),
                        int(row["date_measure"]),
                        float(row["avg_humidity"]),
                        float(row["avg_windspeed"]),
                        float(row["max_temperature"]),
                        float(row["min_temperature"]),
                        float(row["precipitation"])
                    ]
                )
        self.stdout.write("Imported Weather data")

