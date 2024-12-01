from django.db import models

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=80)

    def __str__(self):
        return self.course_name

class Region(models.Model):
    region_id = models.IntegerField(primary_key=True)
    region_name = models.CharField(max_length=10)

    def __str__(self):
        return self.region_name

class Spot(models.Model):
    spot_id = models.IntegerField(primary_key=True)
    spot_name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    course_seq = models.IntegerField()
    time_move = models.IntegerField()
    div_inout = models.CharField(max_length=5)
    tema_name = models.CharField(max_length=50)

    def __str__(self):
        return self.spot_name

class Weather(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    date_measure = models.IntegerField()
    avg_humidity = models.DecimalField(max_digits=5, decimal_places=1)
    avg_windspeed = models.DecimalField(max_digits=5, decimal_places=1)
    max_temperature = models.DecimalField(max_digits=5, decimal_places=1)
    min_temperature = models.DecimalField(max_digits=5, decimal_places=1)
    precipitation = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        unique_together = ('region', 'date_measure')
