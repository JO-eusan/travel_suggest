import csv
from django.core.management.base import BaseCommand
from travel.models import Course, Region, Spot, Weather

class Command(BaseCommand):
    help = "Import CSV data into the database"

    def handle(self, *args, **kwargs):
        self.clear_tables()  # 기존 데이터 초기화
        self.import_courses()
        self.import_regions()
        self.import_spots()
        self.import_weather()
        self.stdout.write(self.style.SUCCESS("Successfully imported all data"))

    def clear_tables(self):
        """초기 데이터를 삭제합니다."""
        Course.objects.all().delete()
        Region.objects.all().delete()
        Spot.objects.all().delete()
        Weather.objects.all().delete()
        self.stdout.write("Cleared all tables")

    def import_courses(self):
        """Course 데이터를 CSV에서 가져옵니다."""
        with open("table/Course.CSV", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 빈 값 처리
                if not row["course_id"].strip() or not row["course_name"].strip():
                    self.stdout.write(f"Skipped row due to missing data: {row}")
                    continue

                # 데이터 삽입
                Course.objects.update_or_create(
                    course_id=int(row["course_id"]),
                    defaults={"course_name": row["course_name"]}
                )
        self.stdout.write("Imported Course data")

    def import_regions(self):
        """Region 데이터를 CSV에서 가져옵니다."""
        with open("table/Region.CSV", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 빈 값 처리
                if not row["region_id"].strip() or not row["region_name"].strip():
                    self.stdout.write(f"Skipped row due to missing data: {row}")
                    continue  # 빈 값이 있는 행은 건너뜀

                # 데이터 삽입
                Region.objects.update_or_create(
                    region_id=int(row["region_id"]),
                    defaults={"region_name": row["region_name"]}
                )
        self.stdout.write("Imported Region data")

    def import_spots(self):
        """Spot 데이터를 CSV에서 가져옵니다."""
        with open("table/Spot.CSV", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 빈 값 처리
                if not row["spot_id"].strip() or not row["spot_name"].strip():
                    self.stdout.write(f"Skipped row due to missing data: {row}")
                    continue

                # 데이터 삽입
                Spot.objects.update_or_create(
                    spot_id=int(row["spot_id"]),
                    defaults={
                        "spot_name": row["spot_name"],
                        "course_id": int(row["course_id"]),
                        "region_id": int(row["region_id"]),
                        "course_seq": int(row["course_seq"]),
                        "time_move": int(row["time_move"]),
                        "div_inout": row["div_inout"],
                        "tema_name": row["tema_name"],
                    }
                )
        self.stdout.write("Imported Spot data")

    def import_weather(self):
        """Weather 데이터를 CSV에서 가져옵니다."""
        with open("table/Weather.CSV", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Weather.objects.update_or_create(
                    region_id=int(row["region_id"]),
                    date_measure=int(row["date_measure"]),
                    defaults={
                        "avg_humidity": float(row["avg_humidity"]),
                        "avg_windspeed": float(row["avg_windspeed"]),
                        "max_temperature": float(row["max_temperature"]),
                        "min_temperature": float(row["min_temperature"]),
                        "precipitation": float(row["precipitation"]),
                    }
                )
        self.stdout.write("Imported Weather data")
