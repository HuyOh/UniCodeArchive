from django.urls import reverse

from .models import Line
from django.http import JsonResponse


def lines(request):
    """
    这个函数用于从数据库中获取所有的线路信息，并将其渲染到'lines.html'模板中。

    参数:
        request (HttpRequest): 用户通过浏览器发送的一个请求对象。

    返回:
        HttpResponse: 包含渲染后的HTML页面的响应对象。
    """
    allLines = Line.objects.all()  # 获取所有的线路信息
    return render(request, 'lines.html', {'lines': allLines})


def stations(request, line_name):
    line = Line.objects.get(name=line_name)  # 获取指定线路对象
    allStations = get_line_stations(line_name)  # 获取线路的车站信息
    return render(request, 'stations.html', {'line': line, 'stations': allStations})


def get_line_stations(line_name):
    line = Line.objects.get(name=line_name)  # 获取指定线路对象

    # 获取该线路上的所有车站及其换乘线路
    stations = Station.objects.filter(stationline__line=line).order_by('stationline__sequence')

    # 获取每个车站的可换乘线路
    for station in stations:
        transfer_lines = Line.objects.filter(stationline__station=station).exclude(name=line_name)
        station.transfer_lines = transfer_lines

    return stations


# 前端选择线路后，返回线路上的所有站点
def get_stations(request):
    selected_line = request.GET.get('line')  # 获取请求参数中的线路名称
    print('selected_line:', selected_line)

    try:
        line = Line.objects.get(name=selected_line)  # 根据线路名称获取对应的线路对象
        station_line_list = StationLine.objects.filter(line=line).order_by('sequence')  # 获取线路对应的站点关系列表，并按照序列顺序排序

        # 构造车站列表
        stations = [station_line.station.name for station_line in station_line_list]

        # 构造JSON响应，将车站列表返回给前端
        response_data = {
            'stations': stations
        }
        print("response_data", response_data)
        return JsonResponse(response_data)
    except Line.DoesNotExist:
        # 处理线路不存在的情况
        error_message = f"Line '{selected_line}' does not exist."
        response_data = {
            'error': error_message
        }
        return JsonResponse(response_data, status=400)


def get_adjacent_stations(station_name):
    adjacent_stations = []
    station_lines = StationLine.objects.filter(station__name=station_name).select_related('line')

    for station_line in station_lines:
        line = station_line.line
        current_sequence = station_line.sequence

        # 获取前一站
        previous_station_line = StationLine.objects.filter(line=line, sequence=current_sequence - 1).first()
        if previous_station_line:
            adjacent_stations.append(previous_station_line.station)

        # 获取后一站
        next_station_line = StationLine.objects.filter(line=line, sequence=current_sequence + 1).first()
        if next_station_line:
            adjacent_stations.append(next_station_line.station)

    return adjacent_stations


def get_line_between_stations(station1_name, station2_name):
    station1_lines = StationLine.objects.filter(station__name=station1_name).values_list('line', flat=True)
    station2_lines = StationLine.objects.filter(station__name=station2_name).values_list('line', flat=True)

    common_lines = set(station1_lines).intersection(station2_lines)

    if common_lines:
        return Line.objects.filter(pk__in=common_lines).first()
    else:
        return None


from collections import deque


def calculate_least_transfer_route(start_station_name, end_station_name):
    # 创建一个队列，用于存储待处理的车站
    queue = deque()
    # 创建一个字典，用于存储每个车站的前一站和所属线路
    previous_station = {}
    # 创建一个字典，用于记录每个车站到起始站的换乘次数
    transfer_count = {start_station_name: 0}

    # 将起始站添加到队列中
    queue.append(start_station_name)

    while queue:
        current_station_name = queue.popleft()

        # 如果当前站是终点站，则已找到完整路径，退出循环
        if current_station_name == end_station_name:
            break

        # 获取当前站的相邻站点
        adjacent_stations = get_adjacent_stations(current_station_name)

        for adjacent_station in adjacent_stations:
            line = get_line_between_stations(current_station_name, adjacent_station.name)

            # 检查相邻站是否已被访问过
            if adjacent_station.name not in previous_station:
                # 更新相邻站的前一站和所属线路
                previous_station[adjacent_station.name] = (current_station_name, line)

                # 计算到达相邻站的换乘次数
                if current_station_name in previous_station:
                    previous_line = previous_station[current_station_name][1]
                    if line != previous_line:
                        transfer_count[adjacent_station.name] = transfer_count[current_station_name] + 1
                    else:
                        transfer_count[adjacent_station.name] = transfer_count[current_station_name]
                else:
                    transfer_count[adjacent_station.name] = transfer_count[current_station_name]

                # 将相邻站添加到队列中
                queue.append(adjacent_station.name)

    # 通过回溯找到完整的乘车路径
    if end_station_name in previous_station:
        route = []
        current = end_station_name
        while current != start_station_name:
            route.append((current, previous_station[current][1].name))
            current = previous_station[current][0]
        route.append((start_station_name, previous_station[start_station_name][1].name))  # 添加起始站，包含线路信息
        route.reverse()  # 反转路径列表，使起始站在最前面

        # 计算线路的总体情况
        total_stations = len(route)
        transfer_count = transfer_count[end_station_name]

        return route, total_stations, transfer_count

    # 如果没有找到路径，则返回空列表和0值
    return [], 0, 0


def calculate_least_station_route(start_station_name, end_station_name):
    # 创建一个队列，用于存储待处理的车站
    queue = deque()
    # 创建一个字典，用于存储每个车站的前一站和所属线路
    previous_station = {}
    # 创建一个字典，用于记录每个车站到起始站的站点数
    station_count = {start_station_name: 0}

    # 将起始站添加到队列中
    queue.append(start_station_name)

    while queue:
        current_station_name = queue.popleft()

        # 如果当前站是终点站，则已找到完整路径，退出循环
        if current_station_name == end_station_name:
            break

        # 获取当前站的相邻站点
        adjacent_stations = get_adjacent_stations(current_station_name)

        for adjacent_station in adjacent_stations:
            line = get_line_between_stations(current_station_name, adjacent_station.name)

            # 检查相邻站是否已被访问过
            if adjacent_station.name not in previous_station:
                # 更新相邻站的前一站和所属线路
                previous_station[adjacent_station.name] = (current_station_name, line)

                # 计算到达相邻站的站点数
                station_count[adjacent_station.name] = station_count[current_station_name] + 1

                # 将相邻站添加到队列中
                queue.append(adjacent_station.name)

    # 通过回溯找到完整的乘车路径
    if end_station_name in previous_station:
        route = []
        current = end_station_name
        while current != start_station_name:
            route.append((current, previous_station[current][1].name))
            current = previous_station[current][0]
        route.append((start_station_name, previous_station[start_station_name][1].name))  # 添加起始站，包含线路信息
        route.reverse()  # 反转路径列表，使起始站在最前面

        # 计算线路的总体情况
        total_stations = station_count[end_station_name] + 1
        transfer_count = 0
        for i in range(len(route) - 1):
            if route[i][1] != route[i + 1][1]:
                transfer_count = transfer_count + 1

        return route, total_stations, transfer_count

    # 如果没有找到路径，则返回空列表和0值
    return [], 0, 0


# 前端点击查询后，获取推荐路线。
def get_route(request):
    # 获取用户选择的出发站和目标站
    start_station = request.POST.get('start-station')
    end_station = request.POST.get('end-station')
    print("start_station", start_station)
    print("end_station", end_station)
    print("request", request)

    # 进行乘车路线的计算，包括最少换乘和最少站点的情况
    # 根据实际情况，调用相应的函数或算法进行计算
    least_transfer_route, total_stations1, transfer_count1 = calculate_least_transfer_route(start_station, end_station)
    least_stations_route, total_stations2, transfer_count2 = calculate_least_station_route(start_station, end_station)
    print("least_transfer_route:", least_transfer_route)
    print("total_stations1:", total_stations1)
    print("transfer_count1:", transfer_count1)
    print("least_stations_route:", least_stations_route)
    print("total_stations2:", total_stations2)
    print("transfer_count2:", transfer_count2)

    # 构造JSON响应，将计算结果返回给前端
    response_data = {
        'total_stations1': total_stations1,
        'transfer_count1': transfer_count1,
        'least_transfer_route': least_transfer_route,
        'total_stations2': total_stations2,
        'transfer_count2': transfer_count2,
        'least_stations_route': least_stations_route,
    }
    return JsonResponse(response_data)


def path_fare(request):
    # 获取所有线路信息，用于渲染选择框
    allLines = Line.objects.all()

    if request.method == 'POST':
        start_line = request.POST.get('start-line')
        end_line = request.POST.get('end-line')
        start_station = request.POST.get('start-station')
        end_station = request.POST.get('end-station')

        print("start_line", start_line)
        print("end_line", end_line)
        print("start_station", start_station)
        print("end_station", end_station)
        print("request", request)

    return render(request, 'path_fare.html', {"lines": allLines})


def announcements(request):
    allAnnouncements = Announcement.objects.all().order_by('-created_time')
    return render(request, 'announcements.html', {'announcements': allAnnouncements})


from django.contrib.auth.hashers import check_password


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("username", username)
        print("password", password)
        try:
            admin = Admin.objects.filter(username=username).first()
            if admin and check_password(password, admin.password):
                # 登录成功，将管理员信息存储在会话中
                request.session['admin_id'] = admin.username
                return redirect('admin_base')  # 跳转到管理员首页
            else:
                messages.error(request, '用户名或密码错误')
        except Admin.DoesNotExist:
            messages.error(request, '用户名或密码错误')
    return render(request, 'login.html')


def admin_base(request):
    return render(request, 'admin_base.html')


def admin_account(request):
    admins = Admin.objects.all()
    return render(request, 'admin_account.html', {'admins': admins})


def edit_admin(request, username):
    admin = Admin.objects.get(username=username)

    if request.method == 'POST':
        # 获取表单提交的数据
        new_username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # 判断新用户名是否与其他管理员的用户名重复
        if Admin.objects.exclude(username=username).filter(username=new_username).exists():
            messages.error(request, '用户名已存在')
            return redirect('edit_admin', username=username)

        # 删除旧账户
        if new_username != username:
            admin.delete()

        # 创建新账户
        new_admin = Admin(username=new_username, password=admin.password, email=email)
        new_admin.save()

        # 判断是否修改了密码
        if password:
            # 使用 make_password 方法对密码进行加密存储
            hashed_password = make_password(password)
            new_admin.password = hashed_password
            new_admin.save()

        messages.success(request, "")
        return redirect('admin_account')  # 重定向到管理员账户页面

    # GET 请求，显示编辑表单
    context = {
        'admin': admin
    }
    return render(request, 'edit_admin.html', context)


from django.contrib import messages


def delete_admin(request, username):
    if request.method == 'POST':
        try:
            admin = Admin.objects.get(username=username)
            admin.delete()
            messages.success(request, '管理员删除成功')
        except Admin.DoesNotExist:
            messages.error(request, '管理员不存在')
    return redirect('admin_account')  # 重定向到管理员账户页面


from .models import Admin
from django.contrib.auth.hashers import make_password


def add_admin(request):
    if request.method == 'POST':
        # 获取表单数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # 创建管理员对象并保存到数据库
        # 在添加管理员时进行密码加密
        password = make_password(request.POST['password'])
        admin = Admin(username=username, password=password, email=email)
        admin.save()

        # 返回添加成功的提示信息
        message = '管理员已成功添加'
        admins = Admin.objects.all()
        return render(request, 'admin_account.html', {'admins': admins, 'message': message})
    else:
        admins = Admin.objects.all()
        return render(request, 'admin_account.html', {'admins': admins})


from django.shortcuts import render, redirect
from .models import Announcement


def admin_announcement(request):
    allAnnouncements = Announcement.objects.all()
    message = request.session.pop('message', None)  # 获取并清除会话中的消息
    return render(request, 'admin_announcement.html', {'announcements': allAnnouncements, 'message': message})


def add_announcement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        new_announcement = Announcement(title=title, content=content)
        new_announcement.save()

        request.session['message'] = '通知公告已添加'
        return redirect('admin_announcement')

    return render(request, 'add_announcement.html')


def edit_announcement(request, announcement_id):
    try:
        announcement = Announcement.objects.get(pk=announcement_id)
    except Announcement.DoesNotExist:
        return redirect('admin_announcement')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        announcement.title = title
        announcement.content = content
        announcement.save()

        request.session['message'] = '通知公告已更新'
        return redirect('admin_announcement')

    return render(request, 'edit_announcement.html', {'announcement': announcement, 'announcement_id': announcement_id})


def delete_announcement(request, announcement_id):
    try:
        announcement = Announcement.objects.get(pk=announcement_id)
        announcement.delete()
        request.session['message'] = '通知公告已删除'
    except Announcement.DoesNotExist:
        pass

    return redirect('admin_announcement')


def admin_lines(request):
    allLines = Line.objects.all()
    context = {'lines': allLines}
    return render(request, 'admin_lines.html', context)


def add_line(request):
    if request.method == 'POST':
        line_name = request.POST.get('line_name')
        line_color = request.POST.get('line_color')
        start_station_name = request.POST.get('start_station')
        end_station_name = request.POST.get('end_station')

        try:
            start_station = Station.objects.get(name=start_station_name)
            end_station = Station.objects.get(name=end_station_name)

            line = Line(name=line_name, color=line_color, start_station=start_station, end_station=end_station)
            line.number = Line.objects.last().number + 1 if Line.objects.exists() else 1  # Generate a unique incrementing value for the number field
            line.save()

            return redirect('admin_lines')  # Redirect to the line management page after adding the line
        except Station.DoesNotExist:
            # Handle the case when the start or end station does not exist
            # You can redirect to an error page or display an error message
            return HttpResponse('Start or end station does not exist.')

    else:
        stations = Station.objects.all()
        context = {'stations': stations}
        return render(request, 'add_line.html', context)



def edit_line(request, line_name):
    line = Line.objects.get(name=line_name)

    if request.method == 'POST':
        new_line_name = request.POST.get('line_name')
        line_color = request.POST.get('line_color')
        start_station_name = request.POST.get('start_station')
        end_station_name = request.POST.get('end_station')

        start_station = Station.objects.get(name=start_station_name)
        end_station = Station.objects.get(name=end_station_name)

        line.name = new_line_name
        line.color = line_color
        line.start_station = start_station
        line.end_station = end_station
        line.save()

        return redirect('/admin_lines/')  # Redirect to the line management page after editing the line
    else:
        stations = StationLine.objects.filter(line=line).order_by('sequence')
        context = {'line': line, 'stations': stations}
        return render(request, 'edit_line.html', context)


def delete_line(request, line_name):
    try:
        line = Line.objects.get(pk=line_name)
        line.delete()
        return redirect('admin_lines')  # Redirect to the admin_lines page after deleting the line
    except Line.DoesNotExist:
        return render(request, 'error.html',
                      {'message': 'Line does not exist'})  # Render an error page if the line does not exist


from django.db import transaction


def edit_station(request, station_name):
    try:
        station = Station.objects.get(name=station_name)
    except Station.DoesNotExist:
        raise Http404("Station does not exist.")

    if request.method == 'POST':
        new_station_name = request.POST.get('station_name')
        longitude = request.POST.get('station_longitude')
        latitude = request.POST.get('station_latitude')

        with transaction.atomic():
            # Update related Line records if the station is the start or end station
            Line.objects.filter(start_station=station_name).update(start_station=new_station_name)
            Line.objects.filter(end_station=station_name).update(end_station=new_station_name)

            # Update related StationLine records
            StationLine.objects.filter(station=station_name).update(station=new_station_name)

            # Update the station fields
            station.name = new_station_name
            station.longitude = longitude
            station.latitude = latitude
            station.save()

        return redirect(reverse('admin_lines'))

    else:
        context = {'station': station}
        return render(request, 'edit_station.html', context)


from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import Station, StationLine


def delete_station(request, station_name):
    # 获取要删除的站点对象
    station = Station.objects.get(name=station_name)

    # 获取与该站点相关的所有站点线路记录
    station_lines = StationLine.objects.filter(station=station)

    # 更新相关线路的起始站和终点站信息
    for station_line in station_lines:
        line = station_line.line
        if line.start_station == station:
            # 如果该站点是线路的起始站，则更新起始站为下一个站点
            next_station_line = StationLine.objects.filter(line=line, sequence=station_line.sequence + 1).first()
            line.start_station = next_station_line.station if next_station_line else None
        if line.end_station == station:
            # 如果该站点是线路的终点站，则更新终点站为上一个站点
            previous_station_line = StationLine.objects.filter(line=line, sequence=station_line.sequence - 1).first()
            line.end_station = previous_station_line.station if previous_station_line else None
        line.save()

    # 从StationLine模型中删除与该站点相关的所有记录
    station_lines.delete()

    # 删除成功后，重定向到管理线路的页面，以展示更新后的数据
    return redirect('admin_lines')


def add_station(request, line_name):
    try:
        line = Line.objects.get(name=line_name)
    except Line.DoesNotExist:
        raise Http404("Line does not exist")

    if request.method == 'POST':
        station_name = request.POST.get('station_name')
        station_longitude = request.POST.get('station_longitude')
        station_latitude = request.POST.get('station_latitude')
        station_sequence = int(request.POST.get('station_sequence'))

        try:
            station = Station.objects.get(name=station_name)
        except Station.DoesNotExist:
            # 如果站点不存在，则创建新的站点对象并保存到数据库
            station = Station(name=station_name, longitude=station_longitude, latitude=station_latitude)
            station.save()

        try:
            station_line = StationLine.objects.get(station=station, line=line)
        except StationLine.DoesNotExist:
            # 如果站点与线路的关联关系不存在，则创建新的关联关系对象并保存到数据库
            station_line = StationLine(station=station, line=line, sequence=station_sequence)
            station_line.save()

            # 获取线路的最小和最大序号的站点
            min_sequence_station = StationLine.objects.filter(line=line).order_by('sequence').first()
            max_sequence_station = StationLine.objects.filter(line=line).order_by('-sequence').first()

            if min_sequence_station and max_sequence_station:
                # 检查新添加的站点序号是否是线路的最小或最大值
                if station_sequence < min_sequence_station.sequence:
                    line.start_station = station
                    line.save()
                elif station_sequence > max_sequence_station.sequence:
                    line.end_station = station
                    line.save()

        return redirect('edit_line', line_name=line.name)

    else:
        return redirect('edit_line', line_name=line.name)
