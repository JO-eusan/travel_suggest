from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Create or replace database views"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE OR REPLACE VIEW course_summary_view AS
                SELECT 
                    c.course_id, 
                    c.course_name,
                    COUNT(s.spot_id) AS spot_count,
                    (SELECT s2.time_move * 10
                     FROM travel_spot s2
                     WHERE s2.course_id = c.course_id
                     ORDER BY s2.course_seq DESC
                     LIMIT 1) AS total_time
                FROM travel_course c
                LEFT JOIN travel_spot s ON c.course_id = s.course_id
                GROUP BY c.course_id, c.course_name;
            """)

            cursor.execute("""
                CREATE OR REPLACE VIEW spot_detail_view AS
                SELECT 
                    s.course_id,
                    s.course_seq, 
                    s.spot_name, 
                    r.region_name, 
                    c.course_name, 
                    s.div_inout, 
                    COALESCE(s.time_move - LAG(s.time_move, 1) OVER (PARTITION BY s.course_id ORDER BY s.course_seq), 0) * 10 AS actual_time
                FROM travel_spot s
                JOIN travel_region r ON s.region_id = r.region_id
                JOIN travel_course c ON s.course_id = c.course_id;
            """)

        self.stdout.write(self.style.SUCCESS("Views created successfully."))
