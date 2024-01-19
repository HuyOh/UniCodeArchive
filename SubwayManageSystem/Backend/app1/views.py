from django.shortcuts import render, HttpResponse


# Create your views here.


def index(request):
    return HttpResponse("欢迎使用!")


def login(request):
    # 去app/templates中找demolist.html,根据app的注册顺序逐一去对应的templates目录中找
    return render(request, "login.html")


def tpl(request):
    name = "韩超"
    roles = ["管理员", "CEO", "保安"]
    user_info = {"name": "郭智", "salary": 100000, 'role': "CTO"}

    data_list = [
        {"name": "郭智", "salary": 100000, 'role': "CTO"},
        {"name": "卢慧", "salary": 100000, 'role': "CTO"},
        {"name": "赵建先", "salary": 100000, 'role': "CTO"},
    ]
    return render(request, 'tpl.html', {"n1": name, "n2": roles, 'n3': user_info, "n4": data_list})


def news(request):
    # 1.定义一些新闻（字典或者列表） 或 去数据库  网络请求去联通新闻
    # 向地址：http://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2021/11/news 发送请求
    # 第三方模块：requests  (pip install requests)
    import requests
    url = 'https://www.10086.cn/aboutus/news/groupnews/5018449_5585_11769.json'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'}
    res = requests.get(url, headers=headers)
    data_list = res.text
    print('回复：', data_list)

    return render(request, 'news.html', {"news_list": data_list})
