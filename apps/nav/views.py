from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import json

from .models import Config

import colorama
JSON_FILE = "apps/nav/static/nav/data.json"


def better_print(var):
    print(colorama.Fore.YELLOW + colorama.Style.BRIGHT +
          str(var) + colorama.Style.RESET_ALL)


def me(request):
    return HttpResponseRedirect("https://linktr.ee/Henry529")


def index(request):
    def get_data(json_file):
        with open(json_file) as f:
            data = dict(json.load(f))
        return data

    def is_vaild(item):
        if len(item) > 0:
            return True
        return False

    def strip_space(item):
        return item.strip()

    data = get_data(JSON_FILE)
    excludeList = []
    if request.user.is_authenticated:
        try:
            excludeList = list(map(strip_space, list(
                filter(is_vaild, Config.objects.get(user=request.user).excludeList.split(',')))))  # 获取配置去掉，和空格
        except:
            excludeList = []
    categories = data["categories"]
    return render(request, "nav/index.html", context={"categories": categories, "excludeList": excludeList})


@login_required(login_url="/")
def config_api(request):
    excludeList = request.POST['excludeList']
    try:
        config = Config.objects.get(user=request.user)
        config.excludeList = excludeList
        config.save()
    except:
        config = Config(user=request.user, excludeList=excludeList)
        config.save()
    return JsonResponse({"excludeList": excludeList})


def resource(request, name):
    CONFIG = [
        {
            "name": "design",
            "title": "设计",
            "items": [
                {"name": "渐变", "url": "https://cssgradient.io/"},
                {"name": "渐变背景色", "url": "https://uigradients.com/#AzurePop"},
                {"name": "背景图", "url": "https://duotone.shapefactory.co/"},
                {"name": "CSS效果", "url": "https://lhammer.cn/You-need-to-know-css/#/zh-cn/"},
                {"name": "CSS Tricks", "url": "https://qishaoxuan.github.io/css_tricks/"},
                {"name": "新拟态效果生成", "url": "https://neumorphism.io/"},
                {"name": "Google font", "url": "https://fonts.google.com/"},
                {"name": "CSS常见效果生成", "url": "https://enjoycss.com/"},
                {"name": "CSS-Inspiration", "url": "https://csscoco.com/inspiration/"},
                {"name": "Logo设计", "url": "https://www.designevo.com/logo-maker/"},
            ]
        },
        {
            "name": "ebook",
            "title": "电子书",
            "items": [
                {"name": "mobi2epub", "url": "https://mobi2epub.com/",
                    "class": "special"},
                {"name": "Kindle Unlimited",
                    "url": "https://www.amazon.cn/kindle-dbs/ku/ku-central"},
                {"name": "鸠摩搜书", "url": "https://www.jiumodiary.com/"},
                {"name": "蓝菊花", "url": "http://www.lanjuhua.com/"},
                {"name": "SoBook", "url": "https://sobooks.cc/"},
                {"name": "Academia", "url": "https://www.academia.edu/"},
                {"name": "hk1lib", "url": "https://hk1lib.org/"},
                {"name": "NOBA", "url": "https://nobaproject.com/"},
                {"name": "free-ebooks", "url": "https://www.free-ebooks.net/"},
            ]
        },
        {
            "name": "game",
            "title": "在线游戏",
            "items": [
                {"name": "井字棋", "url": "https://playtictactoe.org/"},
                {"name": "贪吃蛇", "url": "https://playsnake.org/"},
                {"name": "跳棋", "url": "https://hexxagon.com/"},
                {"name": "人生重开模拟器", "url": "http://liferestart.syaro.io/view/index.html"},
                {"name": "无厘头视频", "url": "https://neave.tv/"},
                {"name": "特效相机", "url": "https://webcamtoy.com/"},
                {"name": "拼音2中文", "url": "https://lab.magiconch.com/nbnhhsh/"},
            ]
        },
        {
            "name": "icon",
            "title": "图标",
            "items": [
                {"name": "OpenMoji", "url": "https://www.openmoji.org/"},
                {"name": "icofont", "url": "https://icofont.com/icons"},
                {"name": "fontawesome", "url": "https://fontawesome.com/v6.0/icons/"},
                {"name": "simpleicons", "url": "https://simpleicons.org/"},
                {"name": "Google Font", "url": "https://fonts.google.com/icons/"},
                {"name": "可定制的开源SVG图标", "url": "https://tablericons.com/"},
                {"name": "icons8", "url": "https://icons8.com/icons"},
                {"name": "Bootstrap自带图标", "url": "https://icons.getbootstrap.com/"},
                {"name": "MacOS图标", "url": "https://macosicons.com/"}
            ]
        },
        {
            "name": "interview",
            "title": "面试",
            "items": [
                {"name": "前端面试常考问题整理 | 按模块和知识点分类",
                    "url": "https://blog.poetries.top/FE-Interview-Questions/"},
                {"name": "WEB前端面试宝典",
                    "url": "https://github.com/h5bp/Front-end-Developer-Interview-Questions/"},
                {"name": "掘金前端面试题合集",
                    "url": "https://github.com/shfshanyue/blog/blob/master/post/juejin-interview.md"},
                {"name": "前端面试图谱", "url": "https://yuchengkai.cn/"},
                {"name": "前端面试开源项目汇总",
                    "url": "https://github.com/biaochenxuying/blog/issues/47"},
                {"name": "简易前端代码规范", "url": "https://codeguide.bootcss.com/"},
                {"name": "京东前端代码规范", "url": "https://guide.aotu.io/index.html"},
                {"name": "LeetCode算法题解",
                    "url": "https://leetcode-solution-leetcode-pp.gitbook.io/leetcode-solution"},
            ]
        },
        {
            "name": "picture",
            "title": "图片",
            "items": [
                {"name": "图像放大", "url": "https://bigjpg.com/", "class": "special"},
                {"name": "图像压缩", "url": "https://tinypng.com/", "class": "special"},
                {"name": "wallpaperup", "url": "https://www.wallpaperup.com/"},
                {"name": "unsplash", "url": "https://unsplash.com/"},
                {"name": "pixabay", "url": "https://pixabay.com/"},
                {"name": "wallhaven", "url": "https://wallhaven.cc/"},
                {"name": "freepik", "url": "https://www.freepik.com/"},
                {"name": "pexels", "url": "https://www.pexels.com/"},
            ]
        },
        {
            "name": "software",
            "title": "软件",
            "items": [
                {"name": "AlternativeTo", "url": "https://alternativeto.net/"},
                {"name": "正版中国", "url": "https://getitfree.cn/"},
                {"name": "异次元软件", "url": "https://www.iplaysoft.com/"},
                {"name": "少数派软件商城", "url": "https://sspai.com/mall"},
                {"name": "麦软", "url": "https://www.mairuan.com/"},
            ]
        },
        {
            "name": "template",
            "title": "网站模版",
            "items": [
                {"name": "W3cschool",
                    "url": "https://www.w3schools.com/w3css/w3css_templates.asp"},
                {"name": "Bootswatch", "url": "https://bootswatch.com/"},
                {"name": "HTML5UP", "url": "https://html5up.net/"},
                {"name": "Themeforest", "url": "https://themeforest.net/"},
                {"name": "Nicepage", "url": "https://nicepage.com/html-templates"},
            ]
        },
        {
            "name": "test",
            "title": "测试",
            "items": [
                {"name": "代理抓包", "url": "https://wproxy.org/whistle/"},
                {"name": "网站测速(可用LH)", "url": "https://www.36ce.net/"},
                {"name": "技术栈检测", "url": "https://www.wappalyzer.com/"},
            ]
        }
    ]
    for each in CONFIG:
        if name == each["name"]:
            title = each["title"]
            items = each["items"]
            return render(request, "nav/resource.html", locals())

    return HttpResponse("？？？没这个资源")
