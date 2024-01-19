from django.db import models


# Create your models here.

class Managers(models.Model):
    username = models.CharField('管理员账号', max_length=30, primary_key=True)
    password = models.CharField('管理员密码', max_length=30, null=False)

    class Meta:
        db_table = 'Managers'


class Stations(models.Model):
    id = models.IntegerField('站点编号', primary_key=True)
    name = models.CharField('站点名称', max_length=40, null=False)
    longitude = models.DecimalField('站点经度', max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField('站点经度', max_digits=8, decimal_places=6, null=True)

    class Meta:
        db_table = 'stations'


class Edges(models.Model):
    id = models.IntegerField('边编号', primary_key=True)
    distance = models.DecimalField('边长度', max_digits=7, decimal_places=5, null=True)

    class Meta:
        db_table = 'edges'


class Lines(models.Model):
    id = models.IntegerField('线路编号', primary_key=True)
    name = models.CharField('线路名称', max_length=100, null=False)
    startStation = models.ForeignKey(Stations, on_delete=models.DO_NOTHING, db_column='station_id')

    class Meta:
        db_table = 'lines'


class LineEdge(models.Model):
    line = models.ForeignKey(Lines, on_delete=models.DO_NOTHING, db_column='line_id')
    edge = models.ForeignKey(Edges, on_delete=models.DO_NOTHING, db_column='edge_id')

    class Meta:
        db_table = 'line_edge'


class EdgeStation(models.Model):
    edge = models.ForeignKey(Edges, on_delete=models.DO_NOTHING, db_column='edge_id')
    station = models.ForeignKey(Stations, on_delete=models.DO_NOTHING, db_column='station_id')

    class Meta:
        db_table = 'edge_station'


class LineStation(models.Model):
    line = models.ForeignKey(Lines, on_delete=models.DO_NOTHING, db_column='line_id')
    station = models.ForeignKey(Stations, on_delete=models.DO_NOTHING, db_column='station_id')

    class Meta:
        db_table = 'line_station'
