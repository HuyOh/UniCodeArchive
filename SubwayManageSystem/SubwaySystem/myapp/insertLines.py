import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoginDemo.settings')
django.setup()
from myapp.models import Line, Station, StationLine
from django.db import transaction

# 清空表
with transaction.atomic():
    Station.objects.all().delete()
    Line.objects.all().delete()
    StationLine.objects.all().delete()

# 1号线
# 车站数据
station_data = [
    {"name": "富锦路", "longitude": 121.424661, "latitude": 31.39226},
    {"name": "友谊西路", "longitude": 121.427726, "latitude": 31.381227},
    {"name": "宝安公路", "longitude": 121.430975, "latitude": 31.369369},
    {"name": "共富新村", "longitude": 121.433936, "latitude": 31.355004},
    {"name": "呼兰路", "longitude": 121.437711, "latitude": 31.339703},
    {"name": "通河新村", "longitude": 121.441498, "latitude": 31.331094},
    {"name": "共康路", "longitude": 121.447455, "latitude": 31.318642},
    {"name": "彭浦新村", "longitude": 121.448141, "latitude": 31.305883},
    {"name": "汶水路", "longitude": 121.449858, "latitude": 31.292242},
    {"name": "上海马戏城", "longitude": 121.452004, "latitude": 31.279846},
    {"name": "延长路", "longitude": 121.455265, "latitude": 31.271409},
    {"name": "中山北路", "longitude": 121.459128, "latitude": 31.258717},
    {"name": "上海火车站", "longitude": 121.455523, "latitude": 31.249692},
    {"name": "汉中路", "longitude": 121.459128, "latitude": 31.2414},
    {"name": "新闸路", "longitude": 121.467882, "latitude": 31.238538},
    {"name": "人民广场", "longitude": 121.472989, "latitude": 31.232814},
    {"name": "黄陂南路", "longitude": 121.47329, "latitude": 31.222502},
    {"name": "陕西南路", "longitude": 121.460115, "latitude": 31.217107},
    {"name": "常熟路", "longitude": 121.451059, "latitude": 31.213033},
    {"name": "衡山路", "longitude": 121.446725, "latitude": 31.20426},
    {"name": "徐家汇", "longitude": 121.438056, "latitude": 31.191522},
    {"name": "上海体育馆", "longitude": 121.436511, "latitude": 31.181903},
    {"name": "漕宝路", "longitude": 121.43458, "latitude": 31.168097},
    {"name": "上海南站", "longitude": 121.43046, "latitude": 31.154693},
    {"name": "锦江乐园", "longitude": 121.414324, "latitude": 31.142059},
    {"name": "莲花路", "longitude": 121.402994, "latitude": 31.130929},
    {"name": "外环路", "longitude": 121.393167, "latitude": 31.120936},
    {"name": "莘庄", "longitude": 121.385184, "latitude": 31.111237},
]

# 线路数据
line_data = {
    "number": 1,
    "name": "1号线",
    "color": "#E70012",
    "start_station": "富锦路",
    "end_station": "莘庄",
    "total_stations": 28,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="富锦路"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="友谊西路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="宝安公路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="共富新村"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="呼兰路"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="通河新村"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="共康路"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="彭浦新村"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="汶水路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="上海马戏城"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="延长路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="中山北路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="上海火车站"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="汉中路"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="新闸路"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="人民广场"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="黄陂南路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="陕西南路"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="常熟路"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="衡山路"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="徐家汇"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="上海体育馆"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="漕宝路"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="上海南站"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="锦江乐园"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="莲花路"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="外环路"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="莘庄"), "line": line, "sequence": 28},
    ]

    StationLine.objects.bulk_create(
        [StationLine(station=item["station"], line=item["line"], sequence=item["sequence"]) for item in
         station_line_data]
    )

# 2号线
# 车站数据
station_data = [
    {"name": "浦东国际机场", "longitude": 121.806436, "latitude": 31.149596},
    {"name": "海天三路", "longitude": 121.796878, "latitude": 31.168459},
    {"name": "远东大道", "longitude": 121.755346, "latitude": 31.199485},
    {"name": "凌空路", "longitude": 121.723791, "latitude": 31.192826},
    {"name": "川沙", "longitude": 121.69821, "latitude": 31.186741},
    {"name": "华夏东路", "longitude": 121.681098, "latitude": 31.196553},
    {"name": "创新中路", "longitude": 121.673133, "latitude": 31.214327},
    {"name": "唐镇", "longitude": 121.656269, "latitude": 31.214107},
    {"name": "广兰路", "longitude": 121.619354, "latitude": 31.211042},
    {"name": "金科路", "longitude": 121.601662, "latitude": 31.204405},
    {"name": "张江高科", "longitude": 121.587687, "latitude": 31.201832},
    {"name": "龙阳路", "longitude": 121.557884, "latitude": 31.204102},
    {"name": "世纪公园", "longitude": 121.552556, "latitude": 31.215723},
    {"name": "上海科技馆", "longitude": 121.544439, "latitude": 31.21882},
    {"name": "世纪大道", "longitude": 121.527221, "latitude": 31.228764},
    {"name": "东昌路", "longitude": 121.515556, "latitude": 31.23327},
    {"name": "陆家嘴", "longitude": 121.502937, "latitude": 31.237991},
    {"name": "南京东路", "longitude": 121.475137, "latitude": 31.232781},
    {"name": "人民广场", "longitude": 121.472894, "latitude": 31.232943},
    {"name": "南京西路", "longitude": 121.459971, "latitude": 31.229853},
    {"name": "静安寺", "longitude": 121.445314, "latitude": 31.223493},
    {"name": "江苏路", "longitude": 121.430635, "latitude": 31.220408},
    {"name": "中山公园", "longitude": 121.416649, "latitude": 31.219879},
    {"name": "娄山关路", "longitude": 121.404058, "latitude": 31.211158},
    {"name": "威宁路", "longitude": 121.387285, "latitude": 31.21487},
    {"name": "北新泾", "longitude": 121.373994, "latitude": 31.216357},
    {"name": "淞虹路", "longitude": 121.359588, "latitude": 31.218212},
    {"name": "虹桥2号航站楼", "longitude": 121.327625, "latitude": 31.194014},
    {"name": "虹桥火车站", "longitude": 121.318911, "latitude": 31.193987},
    {"name": "徐泾东", "longitude": 121.299204, "latitude": 31.188367},
]

# 线路数据
line_data = {
    "number": 2,
    "name": "2号线",
    "color": "#008000",
    "start_station": "浦东国际机场",
    "end_station": "徐泾东",
    "total_stations": 30,
}

# 插入数据
with transaction.atomic():
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    station_line_data = [
        {"station": Station.objects.get(name="浦东国际机场"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="海天三路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="远东大道"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="凌空路"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="川沙"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="华夏东路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="创新中路"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="唐镇"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="广兰路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="金科路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="张江高科"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="龙阳路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="世纪公园"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="上海科技馆"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="世纪大道"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="东昌路"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="陆家嘴"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="南京东路"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="人民广场"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="南京西路"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="静安寺"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="江苏路"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="中山公园"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="娄山关路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="威宁路"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="北新泾"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="淞虹路"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="虹桥2号航站楼"), "line": line, "sequence": 28},
        {"station": Station.objects.get(name="虹桥火车站"), "line": line, "sequence": 29},
        {"station": Station.objects.get(name="徐泾东"), "line": line, "sequence": 30},
    ]

    StationLine.objects.bulk_create(
        [StationLine(**data) for data in station_line_data], ignore_conflicts=True
    )

# 三号线
# 车站数据
station_data = [
    {"name": "上海南站", "longitude": 121.430041, "latitude": 31.154579},
    {"name": "石龙路", "longitude": 121.443205, "latitude": 31.157949},
    {"name": "龙漕路", "longitude": 121.444346, "latitude": 31.16961},
    {"name": "漕溪路", "longitude": 121.43841, "latitude": 31.176746},
    {"name": "宜山路", "longitude": 121.427817, "latitude": 31.186164},
    {"name": "虹桥路", "longitude": 121.420814, "latitude": 31.197524},
    {"name": "延安西路", "longitude": 121.417062, "latitude": 31.209616},
    {"name": "中山公园", "longitude": 121.415683, "latitude": 31.218026},
    {"name": "金沙江路", "longitude": 121.41342, "latitude": 31.232338},
    {"name": "曹杨路", "longitude": 121.417454, "latitude": 31.238943},
    {"name": "镇坪路", "longitude": 121.429856, "latitude": 31.246135},
    {"name": "中潭路", "longitude": 121.441143, "latitude": 31.254316},
    {"name": "上海火车站", "longitude": 121.458052, "latitude": 31.24929},
    {"name": "宝山路", "longitude": 121.476076, "latitude": 31.251491},
    {"name": "东宝兴路", "longitude": 121.480024, "latitude": 31.259782},
    {"name": "虹口足球场", "longitude": 121.479252, "latitude": 31.269613},
    {"name": "赤峰路", "longitude": 121.482427, "latitude": 31.280984},
    {"name": "大柏树", "longitude": 121.483286, "latitude": 31.289273},
    {"name": "江湾镇", "longitude": 121.485174, "latitude": 31.305518},
    {"name": "殷高西路", "longitude": 121.484616, "latitude": 31.319927},
    {"name": "长江南路", "longitude": 121.491182, "latitude": 31.331878},
    {"name": "淞发路", "longitude": 121.500409, "latitude": 31.344817},
    {"name": "张华浜", "longitude": 121.498521, "latitude": 31.3579},
    {"name": "淞滨路", "longitude": 121.492556, "latitude": 31.371019},
    {"name": "水产路", "longitude": 121.488178, "latitude": 31.381095},
    {"name": "宝杨路", "longitude": 121.479466, "latitude": 31.395126},
    {"name": "友谊路", "longitude": 121.475904, "latitude": 31.403844},
    {"name": "铁力路", "longitude": 121.460798, "latitude": 31.407947},
    {"name": "江杨北路", "longitude": 121.439984, "latitude": 31.407617},
]

# 线路数据
line_data = {
    "number": 3,
    "name": "3号线",
    "color": "#FFD100",
    "start_station": "上海南站",
    "end_station": "江杨北路",
    "total_stations": 29,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="上海南站"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="石龙路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="龙漕路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="漕溪路"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="宜山路"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="虹桥路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="延安西路"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="中山公园"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="金沙江路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="曹杨路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="镇坪路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="中潭路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="上海火车站"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="宝山路"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="东宝兴路"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="虹口足球场"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="赤峰路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="大柏树"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="江湾镇"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="殷高西路"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="长江南路"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="淞发路"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="张华浜"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="淞滨路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="水产路"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="宝杨路"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="友谊路"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="铁力路"), "line": line, "sequence": 28},
        {"station": Station.objects.get(name="江杨北路"), "line": line, "sequence": 29},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )


# 4号线
# 车站数据
station_data = [
    {"name": "宜山路", "longitude": 121.427194, "latitude": 31.186717},
    {"name": "上海体育馆", "longitude": 121.436721, "latitude": 31.182311},
    {"name": "上海体育场", "longitude": 121.443588, "latitude": 31.184955},
    {"name": "东安路", "longitude": 121.454917, "latitude": 31.190021},
    {"name": "大木桥路", "longitude": 121.463844, "latitude": 31.194353},
    {"name": "鲁班路", "longitude": 121.474487, "latitude": 31.198685},
    {"name": "西藏南路", "longitude": 121.489507, "latitude": 31.201621},
    {"name": "南浦大桥", "longitude": 121.499635, "latitude": 31.207935},
    {"name": "塘桥", "longitude": 121.51869, "latitude": 31.209623},
    {"name": "蓝村路", "longitude": 121.527627, "latitude": 31.211672},
    {"name": "浦电路(4号线)", "longitude": 121.532044, "latitude": 31.222246},
    {"name": "世纪大道", "longitude": 121.527444, "latitude": 31.228561},
    {"name": "浦东大道", "longitude": 121.51929, "latitude": 31.239423},
    {"name": "杨树浦路", "longitude": 121.51723, "latitude": 31.251898},
    {"name": "大连路", "longitude": 121.51354, "latitude": 31.257474},
    {"name": "临平路", "longitude": 121.500923, "latitude": 31.260189},
    {"name": "海伦路", "longitude": 121.488735, "latitude": 31.258868},
    {"name": "宝山路", "longitude": 121.47689, "latitude": 31.251237},
    {"name": "上海火车站", "longitude": 121.455947, "latitude": 31.249476},
    {"name": "中潭路", "longitude": 121.441184, "latitude": 31.254319},
    {"name": "镇坪路", "longitude": 121.431829, "latitude": 31.246321},
    {"name": "曹杨路", "longitude": 121.417667, "latitude": 31.237735},
    {"name": "金沙江路", "longitude": 121.411315, "latitude": 31.230836},
    {"name": "中山公园", "longitude": 121.415607, "latitude": 31.217551},
    {"name": "延安西路", "longitude": 121.41698, "latitude": 31.20955},
    {"name": "虹桥路", "longitude": 121.422216, "latitude": 31.195968},
]

# 线路数据
line_data = {
    "number": 4,
    "name": "4号线",
    "color": "#471E86",
    "start_station": "宜山路",
    "end_station": "虹桥路",
    "total_stations": 26,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="宜山路"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="上海体育馆"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="上海体育场"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="东安路"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="大木桥路"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="鲁班路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="西藏南路"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="南浦大桥"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="塘桥"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="蓝村路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="浦电路(4号线)"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="世纪大道"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="浦东大道"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="杨树浦路"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="大连路"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="临平路"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="海伦路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="宝山路"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="上海火车站"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="中潭路"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="镇坪路"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="曹杨路"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="金沙江路"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="中山公园"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="延安西路"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="虹桥路"), "line": line, "sequence": 26},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )

# 5号线
# 车站数据
station_data = [
    {"name": "莘庄", "longitude": 121.385379, "latitude": 31.111193},
    {"name": "春申路", "longitude": 121.385937, "latitude": 31.098112},
    {"name": "银都路", "longitude": 121.390143, "latitude": 31.089365},
    {"name": "颛桥", "longitude": 121.401944, "latitude": 31.066945},
    {"name": "北桥", "longitude": 121.409755, "latitude": 31.045033},
    {"name": "剑川路", "longitude": 121.416578, "latitude": 31.026243},
    {"name": "东川路", "longitude": 121.420012, "latitude": 31.018225},
    {"name": "金平路", "longitude": 121.410313, "latitude": 31.011237},
    {"name": "华宁路", "longitude": 121.395292, "latitude": 31.007265},
    {"name": "文井路", "longitude": 121.38083, "latitude": 31.003366},
    {"name": "闵行开发区", "longitude": 121.369715, "latitude": 31.000423},
]

# 线路数据
line_data = {
    "number": 5,
    "name": "5号线",
    "color": "#9253B2",
    "start_station": "莘庄",
    "end_station": "闵行开发区",
    "total_stations": 11,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="莘庄"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="春申路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="银都路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="颛桥"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="北桥"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="剑川路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="东川路"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="金平路"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="华宁路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="文井路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="闵行开发区"), "line": line, "sequence": 11},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )


# 6号线
# 车站数据
station_data = [
    {"name": "港城路", "longitude": 121.574752, "latitude": 31.353005},
    {"name": "外高桥保税区北", "longitude": 121.586768, "latitude": 31.347764},
    {"name": "航津路", "longitude": 121.593892, "latitude": 31.33532},
    {"name": "外高桥保税区南", "longitude": 121.601874, "latitude": 31.321427},
    {"name": "洲海路", "longitude": 121.589386, "latitude": 31.312261},
    {"name": "五洲大道", "longitude": 121.589129, "latitude": 31.302618},
    {"name": "东靖路", "longitude": 121.588528, "latitude": 31.290736},
    {"name": "巨峰路", "longitude": 121.588399, "latitude": 31.280651},
    {"name": "五莲路", "longitude": 121.588013, "latitude": 31.271775},
    {"name": "博兴路", "longitude": 121.586768, "latitude": 31.263154},
    {"name": "金桥路", "longitude": 121.581533, "latitude": 31.256955},
    {"name": "云山路", "longitude": 121.572778, "latitude": 31.250057},
    {"name": "德平路", "longitude": 121.564324, "latitude": 31.245324},
    {"name": "北洋泾路", "longitude": 121.551921, "latitude": 31.238867},
    {"name": "民生路", "longitude": 121.543638, "latitude": 31.235454},
    {"name": "源深体育中心", "longitude": 121.534798, "latitude": 31.232775},
    {"name": "世纪大道", "longitude": 121.527373, "latitude": 31.228298},
    {"name": "浦电路(6号线)", "longitude": 121.529104, "latitude": 31.22008},
    {"name": "蓝村路", "longitude": 121.527846, "latitude": 31.211526},
    {"name": "上海儿童医学中心", "longitude": 121.523297, "latitude": 31.203194},
    {"name": "临沂新村", "longitude": 121.516516, "latitude": 31.193356},
    {"name": "高科西路", "longitude": 121.509778, "latitude": 31.185793},
    {"name": "东明路", "longitude": 121.51098, "latitude": 31.172465},
    {"name": "高青路", "longitude": 121.515658, "latitude": 31.159466},
    {"name": "华夏西路", "longitude": 121.514327, "latitude": 31.14977},
    {"name": "上南路", "longitude": 121.50613, "latitude": 31.148779},
    {"name": "灵岩南路", "longitude": 121.495316, "latitude": 31.148558},
    {"name": "东方体育中心", "longitude": 121.480209, "latitude": 31.153223},
]

# 线路数据
line_data = {
    "number": 6,
    "name": "6号线",
    "color": "#D7006C",
    "start_station": "港城路",
    "end_station": "东方体育中心",
    "total_stations": 28,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="港城路"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="外高桥保税区北"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="航津路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="外高桥保税区南"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="洲海路"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="五洲大道"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="东靖路"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="巨峰路"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="五莲路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="博兴路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="金桥路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="云山路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="德平路"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="北洋泾路"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="民生路"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="源深体育中心"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="世纪大道"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="浦电路(6号线)"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="蓝村路"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="上海儿童医学中心"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="临沂新村"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="高科西路"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="东明路"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="高青路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="华夏西路"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="上南路"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="灵岩南路"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="东方体育中心"), "line": line, "sequence": 28},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )


# 7号线
# 车站数据
station_data = [
    {"name": "花木路", "longitude": 121.562754, "latitude": 31.211212},
    {"name": "龙阳路", "longitude": 121.557304, "latitude": 31.20321},
    {"name": "芳华路", "longitude": 121.550094, "latitude": 31.193005},
    {"name": "锦绣路", "longitude": 121.53988, "latitude": 31.187278},
    {"name": "杨高南路", "longitude": 121.525074, "latitude": 31.187278},
    {"name": "高科西路", "longitude": 121.509711, "latitude": 31.185846},
    {"name": "云台路", "longitude": 121.500527, "latitude": 31.181991},
    {"name": "耀华路", "longitude": 121.494054, "latitude": 31.182001},
    {"name": "长清路", "longitude": 121.486117, "latitude": 31.174611},
    {"name": "后滩", "longitude": 121.473748, "latitude": 31.171967},
    {"name": "龙华中路", "longitude": 121.456968, "latitude": 31.183864},
    {"name": "东安路", "longitude": 121.45465, "latitude": 31.190399},
    {"name": "肇嘉浜路", "longitude": 121.450273, "latitude": 31.199393},
    {"name": "常熟路", "longitude": 121.449028, "latitude": 31.213121},
    {"name": "静安寺", "longitude": 121.44847, "latitude": 31.222736},
    {"name": "昌平路", "longitude": 121.442806, "latitude": 31.233305},
    {"name": "长寿路", "longitude": 121.4383, "latitude": 31.240497},
    {"name": "镇坪路", "longitude": 121.431776, "latitude": 31.246258},
    {"name": "岚皋路", "longitude": 121.422035, "latitude": 31.256164},
    {"name": "新村路", "longitude": 121.422721, "latitude": 31.263684},
    {"name": "大华三路", "longitude": 121.423022, "latitude": 31.273955},
    {"name": "行知路", "longitude": 121.421348, "latitude": 31.284885},
    {"name": "大场镇", "longitude": 121.416541, "latitude": 31.293026},
    {"name": "场中路", "longitude": 121.413537, "latitude": 31.303404},
    {"name": "上大路", "longitude": 121.408559, "latitude": 31.314807},
    {"name": "南陈路", "longitude": 121.398817, "latitude": 31.321296},
    {"name": "上海大学", "longitude": 121.389076, "latitude": 31.320416},
    {"name": "祁华路", "longitude": 121.373626, "latitude": 31.322066},
    {"name": "顾村公园", "longitude": 121.373025, "latitude": 31.344463},
    {"name": "刘行", "longitude": 121.362425, "latitude": 31.3574},
    {"name": "潘广路", "longitude": 121.355988, "latitude": 31.364107},
    {"name": "罗南新村", "longitude": 121.35749, "latitude": 31.388838},
    {"name": "美兰湖", "longitude": 121.350237, "latitude": 31.401623},
]

# 线路数据
line_data = {
    "number": 7,
    "name": "7号线",
    "color": "#FF7F00",
    "start_station": "花木路",
    "end_station": "美兰湖",
    "total_stations": 33,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="花木路"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="龙阳路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="芳华路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="锦绣路"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="杨高南路"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="高科西路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="云台路"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="耀华路"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="长清路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="后滩"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="龙华中路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="东安路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="肇嘉浜路"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="常熟路"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="静安寺"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="昌平路"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="长寿路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="镇坪路"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="岚皋路"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="新村路"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="大华三路"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="行知路"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="大场镇"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="场中路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="上大路"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="南陈路"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="上海大学"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="祁华路"), "line": line, "sequence": 28},
        {"station": Station.objects.get(name="顾村公园"), "line": line, "sequence": 29},
        {"station": Station.objects.get(name="刘行"), "line": line, "sequence": 30},
        {"station": Station.objects.get(name="潘广路"), "line": line, "sequence": 31},
        {"station": Station.objects.get(name="罗南新村"), "line": line, "sequence": 32},
        {"station": Station.objects.get(name="美兰湖"), "line": line, "sequence": 33},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )


# 8号线
# 车站数据
station_data = [
    {"name": "沈杜公路", "longitude": 121.512272, "latitude": 31.061427},
    {"name": "联航路", "longitude": 121.510737, "latitude": 31.07297},
    {"name": "江月路", "longitude": 121.508076, "latitude": 31.084143},
    {"name": "浦江镇", "longitude": 121.505844, "latitude": 31.096345},
    {"name": "芦恒路", "longitude": 121.497862, "latitude": 31.119126},
    {"name": "凌兆新村", "longitude": 121.489451, "latitude": 31.14102},
    {"name": "东方体育中心", "longitude": 121.480181, "latitude": 31.152847},
    {"name": "杨思", "longitude": 121.493399, "latitude": 31.16078},
    {"name": "成山路", "longitude": 121.496146, "latitude": 31.170474},
    {"name": "耀华路", "longitude": 121.494515, "latitude": 31.178038},
    {"name": "中华艺术宫", "longitude": 121.493571, "latitude": 31.184941},
    {"name": "西藏南路", "longitude": 121.489537, "latitude": 31.20146},
    {"name": "陆家浜路", "longitude": 121.486447, "latitude": 31.211151},
    {"name": "老西门", "longitude": 121.483271, "latitude": 31.218638},
    {"name": "大世界", "longitude": 121.479409, "latitude": 31.227006},
    {"name": "人民广场", "longitude": 121.474774, "latitude": 31.232437},
    {"name": "曲阜路", "longitude": 121.470654, "latitude": 31.241977},
    {"name": "中兴路", "longitude": 121.469281, "latitude": 31.252911},
    {"name": "西藏北路", "longitude": 121.469023, "latitude": 31.263183},
    {"name": "虹口足球场", "longitude": 121.47855, "latitude": 31.271693},
    {"name": "曲阳路", "longitude": 121.490996, "latitude": 31.276168},
    {"name": "四平路", "longitude": 121.501467, "latitude": 31.274847},
    {"name": "鞍山新村", "longitude": 121.509878, "latitude": 31.27338},
    {"name": "江浦路", "longitude": 121.518118, "latitude": 31.27448},
    {"name": "黄兴路", "longitude": 121.528504, "latitude": 31.278442},
    {"name": "延吉中路", "longitude": 121.534684, "latitude": 31.288344},
    {"name": "黄兴公园", "longitude": 121.53331, "latitude": 31.295239},
    {"name": "翔殷路", "longitude": 121.532109, "latitude": 31.304699},
    {"name": "嫩江路", "longitude": 121.531508, "latitude": 31.314526},
    {"name": "市光路", "longitude": 121.531765, "latitude": 31.322445},
]

# 8号线
# 线路数据
line_data = {
    "number": 8,
    "name": "8号线",
    "color": "#0000FF",
    "start_station": "沈杜公路",
    "end_station": "市光路",
    "total_stations": 30,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="沈杜公路"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="联航路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="江月路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="浦江镇"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="芦恒路"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="凌兆新村"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="东方体育中心"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="杨思"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="成山路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="耀华路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="中华艺术宫"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="西藏南路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="陆家浜路"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="老西门"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="大世界"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="人民广场"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="曲阜路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="中兴路"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="西藏北路"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="虹口足球场"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="曲阳路"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="四平路"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="鞍山新村"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="江浦路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="黄兴路"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="延吉中路"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="黄兴公园"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="翔殷路"), "line": line, "sequence": 28},
        {"station": Station.objects.get(name="嫩江路"), "line": line, "sequence": 29},
        {"station": Station.objects.get(name="市光路"), "line": line, "sequence": 30},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )

# 9号线
# 车站数据
station_data = [
    {"name": "杨高中路", "longitude": 121.548664, "latitude": 31.22751},
    {"name": "世纪大道", "longitude": 121.527221, "latitude": 31.228764},
    {"name": "商城路", "longitude": 121.516428, "latitude": 31.23014},
    {"name": "小南门", "longitude": 121.498446, "latitude": 31.216837},
    {"name": "陆家浜路", "longitude": 121.486215, "latitude": 31.21179},
    {"name": "马当路", "longitude": 121.477182, "latitude": 31.209514},
    {"name": "打浦桥", "longitude": 121.468792, "latitude": 31.206211},
    {"name": "嘉善路", "longitude": 121.460659, "latitude": 31.202614},
    {"name": "肇嘉浜路", "longitude": 121.450317, "latitude": 31.199218},
    {"name": "徐家汇", "longitude": 121.436884, "latitude": 31.195199},
    {"name": "宜山路", "longitude": 121.427314, "latitude": 31.184387},
    {"name": "桂林路", "longitude": 121.417916, "latitude": 31.174767},
    {"name": "漕河泾开发区", "longitude": 121.397853, "latitude": 31.170508},
    {"name": "合川路", "longitude": 121.384828, "latitude": 31.166469},
    {"name": "星中路", "longitude": 121.368971, "latitude": 31.157986},
    {"name": "七宝", "longitude": 121.34923, "latitude": 31.15525},
    {"name": "中春路", "longitude": 121.337642, "latitude": 31.149373},
    {"name": "九亭", "longitude": 121.319296, "latitude": 31.137252},
    {"name": "泗泾", "longitude": 121.260288, "latitude": 31.117562},
    {"name": "佘山", "longitude": 121.229732, "latitude": 31.103599},
    {"name": "洞泾", "longitude": 121.23059, "latitude": 31.084269},
    {"name": "松江大学城", "longitude": 121.231706, "latitude": 31.053539},
    {"name": "松江新城", "longitude": 121.230676, "latitude": 31.0303},
    {"name": "松江体育中心", "longitude": 121.230333, "latitude": 31.015884},
    {"name": "醉白池", "longitude": 121.229361, "latitude": 31.001125},
    {"name": "松江南站", "longitude": 121.229903, "latitude": 30.982482},
]

# 线路数据
line_data = {
    "number": 9,
    "name": "9号线",
    "color": "#7ac8ee",
    "start_station": "杨高中路",
    "end_station": "松江南站",
    "total_stations": 26,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="杨高中路"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="世纪大道"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="商城路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="小南门"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="陆家浜路"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="马当路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="打浦桥"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="嘉善路"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="肇嘉浜路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="徐家汇"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="宜山路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="桂林路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="漕河泾开发区"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="合川路"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="星中路"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="七宝"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="中春路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="九亭"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="泗泾"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="佘山"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="洞泾"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="松江大学城"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="松江新城"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="松江体育中心"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="醉白池"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="松江南站"), "line": line, "sequence": 26},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )


# 10号线->虹桥火车站
# 车站数据
station_data = [
    {"name": "新江湾城", "longitude": 121.506951, "latitude": 31.328496},
    {"name": "殷高东路", "longitude": 121.506779, "latitude": 31.321714},
    {"name": "三门路", "longitude": 121.508453, "latitude": 31.313245},
    {"name": "江湾体育场", "longitude": 121.514247, "latitude": 31.302648},
    {"name": "五角场", "longitude": 121.514805, "latitude": 31.297955},
    {"name": "国权路", "longitude": 121.510084, "latitude": 31.289373},
    {"name": "同济大学", "longitude": 121.506393, "latitude": 31.282075},
    {"name": "四平路", "longitude": 121.501501, "latitude": 31.27474},
    {"name": "邮电新村", "longitude": 121.49442, "latitude": 31.268247},
    {"name": "海伦路", "longitude": 121.488583, "latitude": 31.259186},
    {"name": "四川北路", "longitude": 121.484163, "latitude": 31.251886},
    {"name": "天潼路", "longitude": 121.482489, "latitude": 31.243814},
    {"name": "南京东路", "longitude": 121.484592, "latitude": 31.238163},
    {"name": "豫园", "longitude": 121.487296, "latitude": 31.227705},
    {"name": "老西门", "longitude": 121.48382, "latitude": 31.219081},
    {"name": "新天地", "longitude": 121.475365, "latitude": 31.216181},
    {"name": "陕西南路", "longitude": 121.458542, "latitude": 31.215007},
    {"name": "上海图书馆", "longitude": 121.444338, "latitude": 31.207923},
    {"name": "交通大学", "longitude": 121.435282, "latitude": 31.202013},
    {"name": "虹桥路", "longitude": 121.422622, "latitude": 31.19625},
    {"name": "宋园路", "longitude": 121.411936, "latitude": 31.19647},
    {"name": "伊犁路", "longitude": 121.403868, "latitude": 31.19871},
    {"name": "水城路", "longitude": 121.392195, "latitude": 31.19926},
    {"name": "龙溪路", "longitude": 121.38005, "latitude": 31.194231},
    {"name": "上海动物园", "longitude": 121.367905, "latitude": 31.190119},
    {"name": "虹桥1号航站楼", "longitude": 121.347263, "latitude": 31.191363},
    {"name": "虹桥2号航站楼", "longitude": 121.326385, "latitude": 31.194226},
    {"name": "虹桥火车站", "longitude": 121.319025, "latitude": 31.193919},
]

# 线路数据
line_data = {
    "number": 10,
    "name": "10号线->虹桥火车站",
    "color": "#C7AFD3",
    "start_station": "新江湾城",
    "end_station": "虹桥火车站",
    "total_stations": 28,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="新江湾城"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="殷高东路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="三门路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="江湾体育场"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="五角场"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="国权路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="同济大学"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="四平路"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="邮电新村"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="海伦路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="四川北路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="天潼路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="南京东路"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="豫园"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="老西门"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="新天地"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="陕西南路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="上海图书馆"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="交通大学"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="虹桥路"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="宋园路"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="伊犁路"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="水城路"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="龙溪路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="上海动物园"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="虹桥1号航站楼"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="虹桥2号航站楼"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="虹桥火车站"), "line": line, "sequence": 28},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )

# 10号线->航中路
# 车站数据
station_data = [
    {"name": "新江湾城", "longitude": 121.506951, "latitude": 31.328496},
    {"name": "殷高东路", "longitude": 121.506779, "latitude": 31.321714},
    {"name": "三门路", "longitude": 121.508453, "latitude": 31.313245},
    {"name": "江湾体育场", "longitude": 121.514247, "latitude": 31.302648},
    {"name": "五角场", "longitude": 121.514805, "latitude": 31.297955},
    {"name": "国权路", "longitude": 121.510084, "latitude": 31.289373},
    {"name": "同济大学", "longitude": 121.506393, "latitude": 31.282075},
    {"name": "四平路", "longitude": 121.501501, "latitude": 31.27474},
    {"name": "邮电新村", "longitude": 121.49442, "latitude": 31.268247},
    {"name": "海伦路", "longitude": 121.488583, "latitude": 31.259186},
    {"name": "四川北路", "longitude": 121.484163, "latitude": 31.251886},
    {"name": "天潼路", "longitude": 121.482489, "latitude": 31.243814},
    {"name": "南京东路", "longitude": 121.484592, "latitude": 31.238163},
    {"name": "豫园", "longitude": 121.487296, "latitude": 31.227705},
    {"name": "老西门", "longitude": 121.48382, "latitude": 31.219081},
    {"name": "新天地", "longitude": 121.475365, "latitude": 31.216181},
    {"name": "陕西南路", "longitude": 121.458542, "latitude": 31.215007},
    {"name": "上海图书馆", "longitude": 121.444338, "latitude": 31.207923},
    {"name": "交通大学", "longitude": 121.435282, "latitude": 31.202013},
    {"name": "虹桥路", "longitude": 121.422622, "latitude": 31.19625},
    {"name": "宋园路", "longitude": 121.411936, "latitude": 31.19647},
    {"name": "伊犁路", "longitude": 121.403868, "latitude": 31.19871},
    {"name": "水城路", "longitude": 121.392195, "latitude": 31.19926},
    {"name": "龙溪路", "longitude": 121.38005, "latitude": 31.194231},
    {"name": "龙柏新村", "longitude": 121.370266, "latitude": 31.176994},
    {"name": "紫藤路", "longitude": 121.364472, "latitude": 31.169687},
    {"name": "航中路", "longitude": 121.355159, "latitude": 31.165354},
]

# 线路数据
line_data = {
    "number": 11,
    "name": "10号线->航中路",
    "color": "#C7AFD3",
    "start_station": "新江湾城",
    "end_station": "航中路",
    "total_stations": 27,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="新江湾城"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="殷高东路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="三门路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="江湾体育场"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="五角场"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="国权路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="同济大学"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="四平路"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="邮电新村"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="海伦路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="四川北路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="天潼路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="南京东路"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="豫园"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="老西门"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="新天地"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="陕西南路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="上海图书馆"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="交通大学"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="虹桥路"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="宋园路"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="伊犁路"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="水城路"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="龙溪路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="龙柏新村"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="紫藤路"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="航中路"), "line": line, "sequence": 27},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )

# 11号线->嘉定北
# 车站数据
station_data = [
    {"name": "迪士尼", "longitude": 121.668162, "latitude": 31.141355},
    {"name": "康新公路", "longitude": 121.616857, "latitude": 31.1305},
    {"name": "秀沿路", "longitude": 121.598146, "latitude": 31.137994},
    {"name": "罗山路", "longitude": 121.592824, "latitude": 31.153053},
    {"name": "御桥", "longitude": 121.570766, "latitude": 31.157974},
    {"name": "浦三路", "longitude": 121.539266, "latitude": 31.150629},
    {"name": "三林东", "longitude": 121.522999, "latitude": 31.146459},
    {"name": "三林", "longitude": 121.511628, "latitude": 31.143063},
    {"name": "东方体育中心", "longitude": 121.480214, "latitude": 31.153127},
    {"name": "龙耀路", "longitude": 121.459722, "latitude": 31.159866},
    {"name": "云锦路", "longitude": 121.458435, "latitude": 31.166255},
    {"name": "龙华", "longitude": 121.453113, "latitude": 31.172498},
    {"name": "上海游泳馆", "longitude": 121.441011, "latitude": 31.178593},
    {"name": "徐家汇", "longitude": 121.435947, "latitude": 31.193719},
    {"name": "交通大学", "longitude": 121.435089, "latitude": 31.202089},
    {"name": "江苏路", "longitude": 121.430711, "latitude": 31.220661},
    {"name": "隆德路", "longitude": 121.423244, "latitude": 31.230349},
    {"name": "曹杨路", "longitude": 121.417493, "latitude": 31.237541},
    {"name": "枫桥路", "longitude": 121.411142, "latitude": 31.241724},
    {"name": "真如", "longitude": 121.406936, "latitude": 31.250677},
    {"name": "上海西站", "longitude": 121.402816, "latitude": 31.26249},
    {"name": "李子园", "longitude": 121.390199, "latitude": 31.269019},
    {"name": "祁连山路", "longitude": 121.376037, "latitude": 31.271514},
    {"name": "武威路", "longitude": 121.364708, "latitude": 31.276429},
    {"name": "桃浦新村", "longitude": 121.349773, "latitude": 31.28127},
    {"name": "南翔", "longitude": 121.322393, "latitude": 31.2966},
    {"name": "马陆", "longitude": 121.277074, "latitude": 31.319479},
    {"name": "嘉定新城", "longitude": 121.254158, "latitude": 31.329964},
    {"name": "白银路", "longitude": 121.245489, "latitude": 31.344919},
    {"name": "嘉定西", "longitude": 121.227378, "latitude": 31.376874},
    {"name": "嘉定北", "longitude": 121.237507, "latitude": 31.391529},
]

# 线路数据
line_data = {
    "number": 12,
    "name": "11号线->嘉定北",
    "color": "#841C21",
    "start_station": "迪士尼",
    "end_station": "嘉定北",
    "total_stations": 31,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="迪士尼"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="康新公路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="秀沿路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="罗山路"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="御桥"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="浦三路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="三林东"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="三林"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="东方体育中心"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="龙耀路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="云锦路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="龙华"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="上海游泳馆"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="徐家汇"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="交通大学"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="江苏路"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="隆德路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="曹杨路"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="枫桥路"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="真如"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="上海西站"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="李子园"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="祁连山路"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="武威路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="桃浦新村"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="南翔"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="马陆"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="嘉定新城"), "line": line, "sequence": 28},
        {"station": Station.objects.get(name="白银路"), "line": line, "sequence": 29},
        {"station": Station.objects.get(name="嘉定西"), "line": line, "sequence": 30},
        {"station": Station.objects.get(name="嘉定北"), "line": line, "sequence": 31},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )


# 11号线->花桥
# 车站数据
station_data = [
    {"name": "迪士尼", "longitude": 121.668162, "latitude": 31.141355},
    {"name": "康新公路", "longitude": 121.616857, "latitude": 31.1305},
    {"name": "秀沿路", "longitude": 121.598146, "latitude": 31.137994},
    {"name": "罗山路", "longitude": 121.592824, "latitude": 31.153053},
    {"name": "御桥", "longitude": 121.570766, "latitude": 31.157974},
    {"name": "浦三路", "longitude": 121.539266, "latitude": 31.150629},
    {"name": "三林东", "longitude": 121.522999, "latitude": 31.146459},
    {"name": "三林", "longitude": 121.511628, "latitude": 31.143063},
    {"name": "东方体育中心", "longitude": 121.480214, "latitude": 31.153127},
    {"name": "龙耀路", "longitude": 121.459722, "latitude": 31.159866},
    {"name": "云锦路", "longitude": 121.458435, "latitude": 31.166255},
    {"name": "龙华", "longitude": 121.453113, "latitude": 31.172498},
    {"name": "上海游泳馆", "longitude": 121.441011, "latitude": 31.178593},
    {"name": "徐家汇", "longitude": 121.435947, "latitude": 31.193719},
    {"name": "交通大学", "longitude": 121.435089, "latitude": 31.202089},
    {"name": "江苏路", "longitude": 121.430711, "latitude": 31.220661},
    {"name": "隆德路", "longitude": 121.423244, "latitude": 31.230349},
    {"name": "曹杨路", "longitude": 121.417493, "latitude": 31.237541},
    {"name": "枫桥路", "longitude": 121.411142, "latitude": 31.241724},
    {"name": "真如", "longitude": 121.406936, "latitude": 31.250677},
    {"name": "上海西站", "longitude": 121.402816, "latitude": 31.26249},
    {"name": "李子园", "longitude": 121.390199, "latitude": 31.269019},
    {"name": "祁连山路", "longitude": 121.376037, "latitude": 31.271514},
    {"name": "武威路", "longitude": 121.364708, "latitude": 31.276429},
    {"name": "桃浦新村", "longitude": 121.349773, "latitude": 31.28127},
    {"name": "南翔", "longitude": 121.322393, "latitude": 31.2966},
    {"name": "马陆", "longitude": 121.277074, "latitude": 31.319479},
    {"name": "嘉定新城", "longitude": 121.254158, "latitude": 31.329964},
    {"name": "上海赛车场", "longitude": 121.225919, "latitude": 31.33198},
    {"name": "昌吉东路", "longitude": 121.20017, "latitude": 31.293739},
    {"name": "上海汽车城", "longitude": 121.180472, "latitude": 31.285524},
    {"name": "安亭", "longitude": 121.161976, "latitude": 31.288458},
    {"name": "兆丰路", "longitude": 121.15026, "latitude": 31.289082},
    {"name": "光明路", "longitude": 121.117043, "latitude": 31.29605},
    {"name": "花桥", "longitude": 121.104211, "latitude": 31.298727},
]

# 线路数据
line_data = {
    "number": 13,
    "name": "11号线->花桥",
    "color": "#841C21",
    "start_station": "迪士尼",
    "end_station": "花桥",
    "total_stations": 35,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="迪士尼"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="康新公路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="秀沿路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="罗山路"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="御桥"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="浦三路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="三林东"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="三林"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="东方体育中心"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="龙耀路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="云锦路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="龙华"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="上海游泳馆"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="徐家汇"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="交通大学"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="江苏路"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="隆德路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="曹杨路"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="枫桥路"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="真如"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="上海西站"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="李子园"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="祁连山路"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="武威路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="桃浦新村"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="南翔"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="马陆"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="嘉定新城"), "line": line, "sequence": 28},
        {"station": Station.objects.get(name="上海赛车场"), "line": line, "sequence": 29},
        {"station": Station.objects.get(name="昌吉东路"), "line": line, "sequence": 30},
        {"station": Station.objects.get(name="上海汽车城"), "line": line, "sequence": 31},
        {"station": Station.objects.get(name="安亭"), "line": line, "sequence": 32},
        {"station": Station.objects.get(name="兆丰路"), "line": line, "sequence": 33},
        {"station": Station.objects.get(name="光明路"), "line": line, "sequence": 34},
        {"station": Station.objects.get(name="花桥"), "line": line, "sequence": 35},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )


# 12号线
# 车站数据
station_data = [
    {"name": "七莘路", "longitude": 121.362464, "latitude": 31.131638},
    {"name": "虹莘路", "longitude": 121.380488, "latitude": 31.137442},
    {"name": "顾戴路", "longitude": 121.391732, "latitude": 31.140748},
    {"name": "东兰路", "longitude": 121.39199, "latitude": 31.155659},
    {"name": "虹梅路", "longitude": 121.397258, "latitude": 31.16025},
    {"name": "虹漕路", "longitude": 121.410561, "latitude": 31.164014},
    {"name": "桂林公园", "longitude": 121.419509, "latitude": 31.16664},
    {"name": "漕宝路", "longitude": 121.432684, "latitude": 31.168145},
    {"name": "龙漕路", "longitude": 121.444443, "latitude": 31.169357},
    {"name": "龙华", "longitude": 121.452683, "latitude": 31.175012},
    {"name": "龙华中路", "longitude": 121.456931, "latitude": 31.184778},
    {"name": "大木桥路", "longitude": 121.463369, "latitude": 31.193883},
    {"name": "嘉善路", "longitude": 121.460751, "latitude": 31.20273},
    {"name": "陕西南路", "longitude": 121.459388, "latitude": 31.216132},
    {"name": "南京西路", "longitude": 121.459292, "latitude": 31.227577},
    {"name": "汉中路", "longitude": 121.458519, "latitude": 31.241668},
    {"name": "曲阜路", "longitude": 121.471437, "latitude": 31.242292},
    {"name": "天潼路", "longitude": 121.482466, "latitude": 31.24376},
    {"name": "国际客运中心", "longitude": 121.497787, "latitude": 31.250034},
    {"name": "提篮桥", "longitude": 121.50667, "latitude": 31.253299},
    {"name": "大连路", "longitude": 121.513108, "latitude": 31.257775},
    {"name": "江浦公园", "longitude": 121.523622, "latitude": 31.264561},
    {"name": "宁国路", "longitude": 121.532248, "latitude": 31.26856},
    {"name": "隆昌路", "longitude": 121.54465, "latitude": 31.275199},
    {"name": "爱国路", "longitude": 121.552761, "latitude": 31.2796},
    {"name": "复兴岛", "longitude": 121.561216, "latitude": 31.280627},
    {"name": "东陆路", "longitude": 121.578983, "latitude": 31.282241},
    {"name": "巨峰路", "longitude": 121.589669, "latitude": 31.28004},
    {"name": "杨高北路", "longitude": 121.602886, "latitude": 31.279894},
    {"name": "金京路", "longitude": 121.615718, "latitude": 31.27949},
    {"name": "申江路", "longitude": 121.626705, "latitude": 31.280114},
    {"name": "金海路", "longitude": 121.638635, "latitude": 31.263131},
]

# 线路数据
line_data = {
    "number": 14,
    "name": "12号线",
    "color": "#057B69",
    "start_station": "七莘路",
    "end_station": "金海路",
    "total_stations": 32,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="七莘路"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="虹莘路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="顾戴路"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="东兰路"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="虹梅路"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="虹漕路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="桂林公园"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="漕宝路"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="龙漕路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="龙华"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="龙华中路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="大木桥路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="嘉善路"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="陕西南路"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="南京西路"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="汉中路"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="曲阜路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="天潼路"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="国际客运中心"), "line": line, "sequence": 19},
        {"station": Station.objects.get(name="提篮桥"), "line": line, "sequence": 20},
        {"station": Station.objects.get(name="大连路"), "line": line, "sequence": 21},
        {"station": Station.objects.get(name="江浦公园"), "line": line, "sequence": 22},
        {"station": Station.objects.get(name="宁国路"), "line": line, "sequence": 23},
        {"station": Station.objects.get(name="隆昌路"), "line": line, "sequence": 24},
        {"station": Station.objects.get(name="爱国路"), "line": line, "sequence": 25},
        {"station": Station.objects.get(name="复兴岛"), "line": line, "sequence": 26},
        {"station": Station.objects.get(name="东陆路"), "line": line, "sequence": 27},
        {"station": Station.objects.get(name="巨峰路"), "line": line, "sequence": 28},
        {"station": Station.objects.get(name="杨高北路"), "line": line, "sequence": 29},
        {"station": Station.objects.get(name="金京路"), "line": line, "sequence": 30},
        {"station": Station.objects.get(name="申江路"), "line": line, "sequence": 31},
        {"station": Station.objects.get(name="金海路"), "line": line, "sequence": 32},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )


# 13号线
# 车站数据
station_data = [
    {"name": "金运路", "longitude": 121.319308, "latitude": 31.240986},
    {"name": "金沙江西路", "longitude": 121.335144, "latitude": 31.240913},
    {"name": "丰庄", "longitude": 121.354928, "latitude": 31.242637},
    {"name": "祁连山南路", "longitude": 121.367202, "latitude": 31.23772},
    {"name": "真北路", "longitude": 121.382093, "latitude": 31.232069},
    {"name": "大渡河路", "longitude": 121.394195, "latitude": 31.231849},
    {"name": "金沙江路", "longitude": 121.411576, "latitude": 31.231042},
    {"name": "隆德路", "longitude": 121.423163, "latitude": 31.230235},
    {"name": "武宁路", "longitude": 121.430158, "latitude": 31.234088},
    {"name": "长寿路", "longitude": 121.438441, "latitude": 31.240913},
    {"name": "江宁路", "longitude": 121.444621, "latitude": 31.244178},
    {"name": "汉中路", "longitude": 121.458654, "latitude": 31.241646},
    {"name": "自然博物馆", "longitude": 121.462259, "latitude": 31.236326},
    {"name": "南京西路", "longitude": 121.462388, "latitude": 31.228546},
    {"name": "淮海中路", "longitude": 121.464405, "latitude": 31.220326},
    {"name": "新天地", "longitude": 121.475219, "latitude": 31.216472},
    {"name": "马当路", "longitude": 121.476893, "latitude": 31.209609},
    {"name": "世博会博物馆", "longitude": 121.4817, "latitude": 31.197606},
    {"name": "世博大道", "longitude": 121.484275, "latitude": 31.182811},
]

# 线路数据
line_data = {
    "number": 15,
    "name": "13号线",
    "color": "#E77DAD",
    "start_station": "金运路",
    "end_station": "世博大道",
    "total_stations": 19,
}

# 插入数据
with transaction.atomic():
    # 插入车站数据
    for station in station_data:
        Station.objects.update_or_create(
            name=station["name"], defaults={"longitude": station["longitude"], "latitude": station["latitude"]}
        )

    # 获取起始和终点车站对象
    start_station = Station.objects.get(name=line_data["start_station"])
    end_station = Station.objects.get(name=line_data["end_station"])

    # 插入线路数据
    line, _ = Line.objects.update_or_create(
        name=line_data["name"],
        defaults={"number": line_data["number"], "color": line_data["color"], "start_station": start_station, "end_station": end_station},
    )

    # 插入车站和线路的关联数据
    station_line_data = [
        {"station": Station.objects.get(name="金运路"), "line": line, "sequence": 1},
        {"station": Station.objects.get(name="金沙江西路"), "line": line, "sequence": 2},
        {"station": Station.objects.get(name="丰庄"), "line": line, "sequence": 3},
        {"station": Station.objects.get(name="祁连山南路"), "line": line, "sequence": 4},
        {"station": Station.objects.get(name="真北路"), "line": line, "sequence": 5},
        {"station": Station.objects.get(name="大渡河路"), "line": line, "sequence": 6},
        {"station": Station.objects.get(name="金沙江路"), "line": line, "sequence": 7},
        {"station": Station.objects.get(name="隆德路"), "line": line, "sequence": 8},
        {"station": Station.objects.get(name="武宁路"), "line": line, "sequence": 9},
        {"station": Station.objects.get(name="长寿路"), "line": line, "sequence": 10},
        {"station": Station.objects.get(name="江宁路"), "line": line, "sequence": 11},
        {"station": Station.objects.get(name="汉中路"), "line": line, "sequence": 12},
        {"station": Station.objects.get(name="自然博物馆"), "line": line, "sequence": 13},
        {"station": Station.objects.get(name="南京西路"), "line": line, "sequence": 14},
        {"station": Station.objects.get(name="淮海中路"), "line": line, "sequence": 15},
        {"station": Station.objects.get(name="新天地"), "line": line, "sequence": 16},
        {"station": Station.objects.get(name="马当路"), "line": line, "sequence": 17},
        {"station": Station.objects.get(name="世博会博物馆"), "line": line, "sequence": 18},
        {"station": Station.objects.get(name="世博大道"), "line": line, "sequence": 19},
    ]

    for data in station_line_data:
        StationLine.objects.update_or_create(
            station=data["station"], line=data["line"], defaults={"sequence": data["sequence"]}
        )
