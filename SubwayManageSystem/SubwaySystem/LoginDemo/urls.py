"""LoginDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from myapp import views


urlpatterns = [
    path('', views.lines, name='lines'),
    path('lines/', views.lines, name='lines'),
    path('stations/<str:line_name>/', views.stations, name='stations'),
    path('path-fare/', views.path_fare, name='path_fare'),
    path('get-stations/', views.get_stations, name='get_stations'),
    path('get_route/', views.get_route, name='get_route'),
    path('announcements/', views.announcements, name='announcements'),
    path('login/', views.login, name='login'),
    path('admin_base/', views.admin_lines, name='admin_base'),
    path('admin_account/', views.admin_account, name='admin_account'),
    path('edit_admin/<str:username>/', views.edit_admin, name='edit_admin'),
    path('delete_admin/<str:username>/', views.delete_admin, name='delete_admin'),
    path('add_admin/', views.add_admin, name='add_admin'),
    path('admin_announcement/', views.admin_announcement, name='admin_announcement'),
    path('add_announcement/', views.add_announcement, name='add_announcement'),
    path('edit_announcement/<int:announcement_id>/', views.edit_announcement, name='edit_announcement'),
    path('delete_announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    path('admin_lines/', views.admin_lines, name='admin_lines'),  # 添加 admin_lines 路径
    path('add_line/', views.add_line, name='add_line'),  # 添加 add_line 路径
    path('edit_line/<str:line_name>/', views.edit_line, name='edit_line'),  # 添加 edit_line 路径
    path('delete_line/<str:line_name>/', views.delete_line, name='delete_line'),  # 添加 edit_line 路径
    path('delete_station/<str:station_name>', views.delete_station, name='delete_station'),
    path('edit_station/<str:station_name>/', views.edit_station, name='edit_station'),
    path('add_station/<str:line_name>/', views.add_station, name='add_station'),
]
