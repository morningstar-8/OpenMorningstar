from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.contrib import auth
from Morningstar.models import User
from django.contrib.auth.decorators import login_required
from django_user_agents.utils import get_user_agent
from django.views.generic import View
from django.contrib import messages
from Morningstar.settings.common import EMAIL_HOST_USER
from django.core.mail import send_mail
import requests
import colorama
import json
import random
import logging
from django_redis import get_redis_connection

from .forms import LoginForm, RegisterForm
from .sms import send_sms_single
from Morningstar.settings.common import TENCENT_SMS_TEMPLATE

DOCKERHUB_DOMAIN = "dockerhub.morningstar529.com"


def better_print(var):
    print(colorama.Fore.YELLOW + colorama.Style.BRIGHT +
          str(var) + colorama.Style.RESET_ALL)


@login_required(login_url="/")
def registry(request):
    try:
        r = requests.get("https://" + DOCKERHUB_DOMAIN + "/v2/_catalog")
        data = dict()
        repos = r.json()["repositories"]
        repo_list = []
        for repo in repos:
            r = requests.get("https://" + DOCKERHUB_DOMAIN +
                             "/v2/" + repo + "/tags/list")
            tags = r.json()["tags"]
            tags = [DOCKERHUB_DOMAIN + "/" + repo + ":" + tag for tag in tags]
            item = dict()
            item["name"] = repo
            item["tags"] = tags
            repo_list.append(item)
        data["domain"] = DOCKERHUB_DOMAIN
        data["repos"] = repo_list
        return render(request, "registry/index.html", context={"data": data})
    except:
        return HttpResponse("服务器未运行")


def shortcut(request, name):
    # VPS托管服务
    if name in ["frps", "beancount", "code", "dockerhub", "ghost", "gitea", "jellyfin", "jupyter", "nextcloud", "portainer", "rsshub", "send", "ssh"]:
        if name == 'dockerhub':
            return HttpResponseRedirect("https://dockerhub.morningstar529.com/v2/_catalog")
        return HttpResponseRedirect("https://" + name + ".morningstar529.com/")
    # 第三方托管服务
    elif name in ["docs", "icofont"]:
        return redirect("https://" + name + ".morningstar529.com/")
    # 项目快捷链接
    elif name in ["issue", "auto", "src", "host", "vercel", "domain", "namecheap", "license", "coverage", "task", "resume", "mailbox"]:
        if name == 'issue':
            return redirect("https://github.com/HenryJi529/OpenMorningstar/issues")
        elif name == "auto":
            return redirect("https://github.com/HenryJi529/OpenMorningstar/actions")
        elif name == "src":
            return redirect("https://github.com/HenryJi529/OpenMorningstar")
        elif name == "host" or name == "vercel":
            return redirect("https://vercel.com/dashboard")
        elif name == "domain" or name == "namecheap":
            return redirect("https://ap.www.namecheap.com/Domains/DomainControlPanel/morningstar529.com/advancedns")
        elif name == "license":
            return redirect("https://cdn.jsdelivr.net/gh/HenryJi529/OpenMorningstar@main/LICENSE")
        elif name == "coverage":
            return redirect("https://coverage.morningstar529.com/")
        elif name == "task":
            return redirect("https://ticktick.com/webapp#m/all/matrix")
        elif name == "resume":
            return redirect("https://resume.morningstar529.com/")
        elif name == "mailbox":
            return redirect("https://privateemail.com/appsuite/#!!&app=io.ox/mail&folder=default0/INBOX")
        else:
            pass
    # 静态资源管理
    elif name in ["jsdelivr", "qiniu", "lanzou"]:
        if name == "jsdelivr":
            return redirect("https://github.com/HenryJi529/OpenMorningstarStatic/")
        elif name == "qiniu":
            return redirect("https://portal.qiniu.com/kodo/bucket/resource-v2?bucketName=morningstar-529")
        elif name == "lanzou":
            return redirect("https://pc.woozooo.com/mydisk.php")
        else:
            pass
    # 速查表链接
    elif name in ["css", "js", "bs", "bash"]:
        if name == "css":
            return HttpResponseRedirect("https://man.ilovefishc.com/css3/")
        elif name == "js":
            return HttpResponseRedirect("https://zh.javascript.info/")
        elif name == "bs":
            return redirect("https://v5.bootcss.com/docs/5.1/getting-started/introduction/")
        elif name == "bash":
            return redirect("https://wsgzao.github.io/post/bash/")
        else:
            pass
    # 娱乐快捷链接
    elif name in ["sgs", "nunu"]:
        if name == "sgs":
            return redirect("https://web.sanguosha.com/login/index.html")
        elif name == "nunu":
            return redirect("https://www.nunuyy1.top/")
        else:
            pass
    else:
        return redirect("https://google.com")


def index(request):
    logger = logging.getLogger("django")
    if request.user.is_authenticated:
        logger.info("已认证进入首页...")
        return render(request, "base/home.html")
    else:
        logger.info("未认证进入首页...")
        try:
            # 判断confirm_password是否在POST中，如果在则注册
            if request.POST["confirm_password"]:
                pass
            logger.info("现在是注册")
            form = RegisterForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                confirm_password = form.cleaned_data.get('confirm_password')

                if User.objects.filter(email=email).exists():
                    messages.add_message(request, messages.ERROR, "此邮箱已注册")
                    return HttpResponseRedirect("/")

                if User.objects.filter(username=username).exists():
                    messages.add_message(request, messages.ERROR, "此用户名已注册")
                    return HttpResponseRedirect("/")

                if password != confirm_password:
                    messages.add_message(
                        request, messages.ERROR, "两次密码不一致")
                    return HttpResponseRedirect("/")

            def create_activate_message(username):
                code = random.randint(10000, 99999)
                conn = get_redis_connection("redis")
                try:
                    conn.delete(f'{username}-activate')
                except:
                    pass
                conn.set(f'{username}-activate', code, ex=60*5)
                return f"通过该链接激活:\nhttps://morningstar529.com/activate/?username={username}&code={code}\n五分钟内有效"

            user = User.objects.create(
                username=username, password=make_password(password), email=email, is_active=False)
            subject = "激活邮件"
            message = create_activate_message(username)
            from_email = EMAIL_HOST_USER
            send_mail(
                subject,
                message,
                from_email,
                [email],
            )
            messages.add_message(
                request, messages.INFO, "注册已完成...请通过邮箱激活")
            return redirect("/")

        except:
            logger.info("现在是登录")
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = auth.authenticate(
                    username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    logger.info("身份验证成功...")
                    next = request.POST.get("next", "/")
                    return redirect(next if next else "/")
                else:
                    messages.add_message(request, messages.ERROR, "用户名或密码错误")
                    return HttpResponseRedirect("/")
        login_form = LoginForm()
        register_form = RegisterForm()
        return render(request, "base/login_register.html", context={
            "login_form": login_form,
            "register_form": register_form,
        })


def login(request):
    auth.logout(request)
    login_form = LoginForm()
    register_form = RegisterForm()
    return render(request, "base/login_register.html", context={
        "login_form": login_form,
        "register_form": register_form,
    })


@login_required(login_url="/")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url="/")
def sms(request):
    tpl = request.GET.get('tpl')
    template_id = TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('模版不存在')
    code = random.randint(10000, 99999)
    res = send_sms_single('19850052801', template_id, [code, ])
    if res['result'] == 0:
        return HttpResponse("Done!")
    else:
        return HttpResponse(res['errmsg'])


def setKey(request, value):
    conn = get_redis_connection("redis")
    conn.set('nickname', value, ex=10)
    return HttpResponse("设置成功，值为：" + value)


def getKey(request):
    conn = get_redis_connection("redis")
    value = conn.get('nickname')
    if not value:
        return HttpResponse("数据已经超时")
    else:
        return HttpResponse("设置成功，值为：" + str(value.decode()))


def activate(request):
    if request.method == "GET":
        username = request.GET["username"]
        code = request.GET["code"]
        conn = get_redis_connection("redis")
        redis_code_bin = conn.get(f'{username}-activate')
        if not redis_code_bin:
            return HttpResponse("激活链接已经超时")
        else:
            redis_code = str(redis_code_bin.decode())
            if code == redis_code:
                user = User.objects.get(username=username)
                user.is_active = True
                user.save()
                conn.delete(f'{username}-activate')
                auth.login(request, user)
                return redirect("/")
            else:
                return HttpResponse("错误的激活链接")
    else:
        return HttpResponse("这是啥玩意儿。。")
