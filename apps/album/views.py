from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Photo


def home(request):
    photos = Photo.objects.all()
    context = {'photos': photos}

    # 处理登入登出的POST请求
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # 登入
        if user is not None and user.is_superuser:
            login(request, user)
        # 登出
        isLogout = request.POST.get('isLogout')
        if isLogout == 'True':
            logout(request)

    return render(request, 'album/list.html', context)


def upload(request):
    if request.method == 'POST' and request.user.is_superuser:
        if request.POST["foreignUrl"]:
            photo = Photo(foreignUrl=request.POST["foreignUrl"])
            photo.save()
            return redirect('album:home')
        images = request.FILES.getlist('images')
        for i in images:
            photo = Photo(image=i)
            photo.save()
    return redirect('album:home')
