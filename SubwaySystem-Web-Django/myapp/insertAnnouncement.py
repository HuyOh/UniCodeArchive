import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoginDemo.settings')
django.setup()

from django.utils import timezone
from myapp.models import Announcement


def generate_sample_announcements():
    announcements = [
        {
            'title': '重要通知',
            'content': '这是一条重要的通知内容。',
            'created_time': timezone.now()
        },
        {
            'title': '暑期运营时间调整',
            'content': '由于暑期学校放假，地铁运营时间将有所调整，请留意。',
            'created_time': timezone.now()
        },
        {
            'title': '新线路开通',
            'content': '我们很高兴地宣布新线路将于下个月开通运营，敬请期待。',
            'created_time': timezone.now()
        }
    ]

    for announcement_data in announcements:
        announcement = Announcement.objects.create(
            title=announcement_data['title'],
            content=announcement_data['content'],
            created_time=announcement_data['created_time']
        )
        announcement.save()


# 调用函数生成示例公告并插入到数据库中
generate_sample_announcements()
