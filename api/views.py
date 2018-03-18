# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from urlparse import urlparse
from api import params
import models
from django.shortcuts import redirect
from django.http import Http404

# Create your views here.
@api_view(['POST'])
def short_url(request):
    response = {
        "status": "",
        "status_codes": []
    }
    post_data = request.data
    if "long_url" not in post_data:
        response['status'] = 'FAILED'
        response['status_codes'] = ["BAD_DATA"]
        return JsonResponse(response)
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

@api_view(['POST'])
def long_url(request):
    response = {
        "status": "",
        "status_codes": []
    }
    post_data = request.data
    if "short_url" not in post_data:
        response['status'] = 'FAILED'
        response['status_codes'] = ["BAD_DATA"]
        return JsonResponse(response)
    short_url = post_data.get('short_url','').rstrip('/')
    unique_hash = short_url.split(params.BASE_URL)[-1]

    try:
        url = models.URL.objects.get(unique_hash=unique_hash)
    except:
        response['status'] = 'FAILED'
        response['status_codes'] = ["SHORT_URLS_NOT_FOUND"]
        return JsonResponse(response)

    long_url = url.long_url
    response['long_url'] = long_url
    response['status'] = 'OK'
    return JsonResponse(response)

@api_view(['POST'])
def short_urls(request):
    response = {
        "status": "",
        "status_codes": [],
        "invalid_urls" : []
    }
    post_data = request.data
    long_urls = post_data.get('long_urls',[])

    if 'long_urls' not in post_data or type(long_urls) is not list:
        response['status'] = 'FAILED'
        response['status_codes'] = ["BAD_DATA"]
        return JsonResponse(response)

    invalid_urls = []
    long_urls = [i.rstrip('/') for i in long_urls ]
    valid_url = True
    valid_long_urls = []
    for long_url in long_urls:
        try:
            valid_url = bool(urlparse(long_url).scheme)
        except:
            valid_url = False
        if valid_url:
            valid_long_urls.append(long_url)
        else:
            invalid_urls.append(long_url)

    urls = models.URL.objects.filter(long_url__in=valid_long_urls).values('long_url','unique_hash')
    short_urls = {}
    for url in urls:
        short_urls[url['long_url']] = params.BASE_URL+str(url['unique_hash'])

    found_urls = [o['long_url'] for o in urls]
    new_urls = [i for i in valid_long_urls if i not in found_urls ]
    for n in new_urls:
        u = models.URL(
            long_url = n
        )
        u.save()
        short_urls[n] = params.BASE_URL+str(u.unique_hash)

    response["short_urls"] = short_urls
    if not valid_url:
        response["invalid_urls"] = invalid_urls
        response["status"] = "FAILED"
        response["status_codes"] = ["INVALID_URLS"]
    else:
        response["status"] = "OK"
    return JsonResponse(response)

@api_view(['POST'])
def long_urls(request):
    response = {
        "status": "",
        "status_codes": [],
        "invalid_urls" : []
    }
    post_data = request.data
    short_urls = post_data.get('short_urls',[])

    if 'short_urls' not in post_data or type(short_urls) is not list:
        response['status'] = 'FAILED'
        response['status_codes'] = ["BAD_DATA"]
        return JsonResponse(response)

    short_urls_dict = { s.rstrip('/').split(params.BASE_URL)[-1]:s for s in short_urls }
    short_urls = [s.rstrip('/').split(params.BASE_URL)[-1] for s in short_urls]
    urls = models.URL.objects.filter(unique_hash__in=short_urls).values('long_url', 'unique_hash')
    long_urls = {}
    for url in urls:
        long_urls[params.BASE_URL+url['unique_hash']] = url['long_url']
    response["long_urls"] = long_urls
    found_urls = [o['unique_hash'] for o in urls]
    new_urls = [short_urls_dict[s] for s in short_urls if s not in found_urls]

    if new_urls:
        response["invalid_urls"] = new_urls
        response["status"] = "FAILED"
        response["status_codes"] = ["INVALID_URLS"]
    else:
        response["status"] = "OK"
    return JsonResponse(response)


def url_redirect(request, unique_hash=""):
    try:
        url = models.URL.objects.get(unique_hash=unique_hash.rstrip('/'))
        url.count = url.count + 1
        url.save()
        long_url = url.long_url
    except:
        raise Http404()
    return redirect(long_url)

@api_view(['POST'])
def count(request):
    response = {
        "status": '',
        "status_codes": []
    }

    post_data = request.data
    if 'short_url' not in post_data:
        response['status'] = 'FAILED'
        response['status_codes'] = ["BAD_DATA"]
        return JsonResponse(response)
    short_url = post_data.get('short_url','').rstrip('/')
    unique_hash = short_url.split(params.BASE_URL)[-1]
    try:
        url = models.URL.objects.get(unique_hash=unique_hash)
    except:
        response['status'] = 'FAILED'
        response['status_codes'] = ["SHORT_URLS_NOT_FOUND"]
        return JsonResponse(response)

    response["count"] = url.count
    response['status'] = 'OK'
    return JsonResponse(response)

def clean_urls(request):
    response = {
        "status": '',
        "status_codes": []
    }
    try:
        models.URL.objects.all().delete()
    except:
        response['status'] = 'FAILED'
        return JsonResponse(response)
    response['status'] = 'OK'
    return JsonResponse(response)
