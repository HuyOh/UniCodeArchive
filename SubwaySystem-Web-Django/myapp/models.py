from django.db import models


# 车站
class Station(models.Model):
    name = models.CharField(max_length=100, primary_key=True)  # 主键字段：车站名
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # 经度
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # 纬度

    def __str__(self):
        return self.name


# 线路
class Line(models.Model):
    number = models.PositiveIntegerField(unique=True)  # 唯一且递增的非主键字段
    name = models.CharField(max_length=100, primary_key=True)  # 主键字段：线路名
    color = models.CharField(max_length=20)  # 线路颜色
    start_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='lines_starting_here',
                                      db_column='start_station')  # 起始车站
    end_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='lines_ending_here',
                                    db_column='end_station')  # 终止车站

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['number']  # 按照number字段升序排序q


# 车站和线路的关系
class StationLine(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, db_column='station')  # 车站
    line = models.ForeignKey(Line, on_delete=models.CASCADE, db_column='line')  # 线路
    sequence = models.IntegerField()  # 车站在线路的顺序

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['station', 'line'], name='station_line_unique')
        ]


# 管理员
class Admin(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username


# 公告
class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
