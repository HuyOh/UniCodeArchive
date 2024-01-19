# views.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoginDemo.settings')
django.setup()

from myapp.models import Line, Station, StationLine
import json

# 获取所有车站信息
stations = Station.objects.all()

# 获取所有边的信息，包含线路颜色信息
station_lines = StationLine.objects.select_related('station', 'line')
edges = []
for station_line in station_lines:
    start_station = station_line.station
    next_station_line = StationLine.objects.filter(line=station_line.line, sequence=station_line.sequence + 1).first()
    if next_station_line:
        end_station = next_station_line.station
        line_color = station_line.line.color
        edge = {
            'start_station': {
                'name': start_station.name,
                'longitude': float(start_station.longitude),
                'latitude': float(start_station.latitude)
            },
            'end_station': {
                'name': end_station.name,
                'longitude': float(end_station.longitude),
                'latitude': float(end_station.latitude)
            },
            'line_color': line_color,
            'line-name': station_line.line.name
        }
        edges.append(edge)

print(stations)
print(edges)

# 将数据转换为 JSON 格式传递给模板
stations_json = json.dumps([{
    'name': station.name,
    'longitude': float(station.longitude),
    'latitude': float(station.latitude)
} for station in stations])
edges_json = json.dumps(edges)

print(stations_json)
print(edges_json)
