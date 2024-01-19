import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoginDemo.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from myapp.models import Admin


def create_admin():
    username = 'root'
    password = '123456'
    email = 'admin@example.com'

    # 使用 make_password 方法对密码进行加密存储
    hashed_password = make_password(password)

    # 创建管理员对象并保存到数据库
    admin = Admin(username=username, password=hashed_password, email=email)
    admin.save()


# 调用函数创建初始管理员
create_admin()
