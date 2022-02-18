from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from Morningstar.models import User
# TODO: 定制此表单[placeholder, label, help_text, max_length, min_length, required]
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm


def loginPage(request):
    page = 'login'
    # NOTE: 已登录用户自动跳转到首页
    if request.user.is_authenticated:
        return redirect("forum:home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.add_message(request, messages.ERROR, "用户不存在")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("forum:home")
        else:
            messages.add_message(request, messages.ERROR, "用户名或密码错误")
    return render(request, 'forum/login_register.html', context={"page": page})


def logoutUser(request):
    logout(request)
    return redirect("forum:home")


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # NOTE: 可对用户名等进行预处理
            user.save()
            login(request, user)
            return redirect('forum:login')
        else:
            messages.add_message(request, messages.ERROR, "注册失败")
    return render(request, 'forum/login_register.html', context={"form": form})


def home(request):
    q = request.GET.get('q', '')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]  # NOTE: 取前5个
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    return render(request, 'forum/home.html', context={
        'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages
    })


def room(request, pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.message_set.all()  # NOTE: 寻找使用(外链)了该room对象的所有message对象
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            owner=request.user,
            room=room,
            body=request.POST["body"]
        )
        room.participants.add(request.user)
        return redirect("forum:room", pk=room.pk)  # NOTE: 选择重定向是为了清理POST数据
    # NOTE: 此处与Django自带messages重复，需替换变量名
    return render(request, 'forum/room.html', context={'room': room, 'room_messages': room_messages, "participants": participants})


@login_required(login_url='forum:login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect("forum:home")
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect("forum:home")
    return render(request, 'forum/room_form.html', context={"form": form, "topics": topics})


@login_required(login_url='forum:login')
def updateRoom(request, pk):
    room = Room.objects.get(pk=pk)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("你不被允许进行此操作")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.filter(pk=pk).update(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect("forum:home")
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect("forum:home")
    return render(request, 'forum/room_form.html', context={"form": RoomForm(instance=room), "topics": topics, "room": room})


@login_required(login_url='forum:login')
def deleteRoom(request, pk):
    room = Room.objects.get(pk=pk)
    if request.user != room.host:
        return HttpResponse("你不被允许进行此操作")
    if request.method == 'POST':
        room.delete()
        return redirect("forum:home")
    return render(request, "forum/delete.html", context={"obj": room})


@login_required(login_url='forum:login')
def deleteMessage(request, pk):
    message = Message.objects.get(pk=pk)
    if request.user != message.owner:
        return HttpResponse("你不被允许进行此操作")
    if request.method == 'POST':
        message.delete()
        return redirect("forum:home")
    # TODO: 需要继续跳转到房间
    return render(request, "forum/delete.html", context={"obj": message})


def userProfile(request, pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    return render(request, "forum/profile.html", context={
        "user": user, "rooms": rooms, "room_messages": room_messages, "topics": topics
    })


@login_required(login_url='forum:login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("forum:user-profile", pk=user.pk)
    return render(request, "forum/update_user.html", {'form': form, })


def topicsPage(request):
    q = request.GET.get('q', '')
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "forum/topics.html", {"topics": topics})


def activitiesPage(request):
    room_messages = Message.objects.all()
    return render(request, "forum/activities.html", {"room_messages": room_messages})
