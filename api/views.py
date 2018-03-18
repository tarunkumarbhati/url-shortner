# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from urlparse import urlparse
from api import params
import models

# Create your views here.
def index(request):
    response = {
        "status":"OK"
    }

    return JsonResponse(response)


@api_view(['POST'])
def short_url(request):
    response = {
        "status": "",
        "status_codes": []
    }
    post_data = request.data

    long_url = post_data.get('long_url','').rstrip('/')
    try:
        valid_url = bool(urlparse(long_url).scheme)
    except:
        valid_url = False

    if not valid_url:
        response['status'] = 'FAILED'
        response['status_codes'] = ["INVALID_URLS"]
        return JsonResponse(response)

    url,_ = models.URL.objects.get_or_create(
        long_url = long_url
    )

    short_url = params.BASE_URL+str(url.unique_hash)
    response['short_url'] = short_url
    response['status'] = 'OK'
    return JsonResponse(response)
