from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    # other fields as needed

    def __str__(self):
        return self.name


class Line(models.Model):
    number = models.PositiveIntegerField(unique=True)  # 唯一且递增的非主键字段
    name = models.CharField(max_length=100, primary_key=True)
    color = models.CharField(max_length=20)
    start_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='lines_starting_here',
                                      db_column='start_station')
    end_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='lines_ending_here',
                                    db_column='end_station')

    # other fields as needed

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['number']  # 按照number字段升序排序q


class StationLine(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, db_column='station')
    line = models.ForeignKey(Line, on_delete=models.CASCADE, db_column='line')
    sequence = models.IntegerField()

    # other fields as needed

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['station', 'line'], name='station_line_unique')
        ]


class Admin(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    # other fields as needed

    def __str__(self):
        return self.username


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    # other fields as needed

    def __str__(self):
        return self.title
