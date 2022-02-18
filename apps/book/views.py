from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render, reverse
import os
import json
JSON_FILE = "apps/book/static/book/data.json"


def index(request):
    def get_data(json_file):
        with open(json_file) as f:
            data = dict(json.load(f))
        return data
    data = get_data(JSON_FILE)
    categories = data['categories']
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'Morningstar.settings.dev':
        endpoint = "http://" + request.META["HTTP_HOST"] + "/book/api/"
    else:
        endpoint = "https://" + request.META["HTTP_HOST"] + "/book/api/"
    return render(request, "book/index.html", locals())


def api(request):
    def get_data(json_file):
        with open(json_file) as f:
            data = dict(json.load(f))
        return data
    data = get_data(JSON_FILE)
    return JsonResponse(data)
