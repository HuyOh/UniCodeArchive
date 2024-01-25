## 准备Django
```commandline
pip install django
```

## 建立django项目
```commandline
django-admin startproject Backend
```

## 创建应用
```commandline
python manage.py startapp "appName"
```

## 创建数据库
- 在Backend/settings.py中设置默认数据库以及app
- 在app/__init__.py中添加
```commandline
import pymysql
pymysql.install_as_MySQLdb()
```

- 在mysql中建立对应数据库
```commandline
create database subwaydb default character set utf8
```

- 同步数据
```commandline
python manage.py makemigrations
python manage.py migrate
```