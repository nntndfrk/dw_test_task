# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import json
import ast
import datetime
import locale

locale.setlocale(locale.LC_TIME, "uk_UA.utf8")

from dwapi import datawiz
from dwutils import MainData, ProductsData, MyEncoder

from django.conf import settings

dw = datawiz.DW(settings.DW_LOGIN, settings.DW_PASSWORD)
user_info = dw.get_client_info()
categorys = dw.get_category()['results'][0]['children']

# Маг-ни з назвою 'Bizare' не повертають даних
shops = {k: v for k, v in user_info[u'shops'].items() if not v.startswith(u'Bizare')}
allshops_list = [shop for shop, name in shops.iteritems()]
allcategorys_list = [int(cat.items()[0][0]) for cat in categorys]

# DW




def index(request):
    return render(request, 'index.html', {'user_info': user_info, 'categorys': categorys, 'shops': shops})


def main_data(request):
    if request.method == "POST":
        shops = [int(n.strip()) for n in ast.literal_eval(request.POST["shops"])]
        category = [int(n.strip()) for n in ast.literal_eval(request.POST["category"])]
        date1 = datetime.datetime.strptime(request.POST["date1"], '%d/%m/%Y')
        date2 = datetime.datetime.strptime(request.POST["date2"], '%d/%m/%Y')
        if not shops:
            shops = allshops_list
        if not category:
            category = allcategorys_list

        data = MainData(dw=dw, categories=category, shops=shops, date1=date1, date2=date2).get_main_data
        return HttpResponse(json.dumps(data, cls=MyEncoder))
    else:
        return HttpResponse("bad")


def products_data(request):
    if request.method == "POST":
        shops = [int(n.strip()) for n in ast.literal_eval(request.POST["shops"])]
        category = [int(n.strip()) for n in ast.literal_eval(request.POST["category"])]
        date1 = datetime.datetime.strptime(request.POST["date1"], '%d/%m/%Y')
        date2 = datetime.datetime.strptime(request.POST["date2"], '%d/%m/%Y')
        if not shops:
            shops = allshops_list
        if not category:
            category = allcategorys_list

        data = ProductsData(dw=dw, categories=category, shops=shops, date1=date1, date2=date2).get_prod_data
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("bad")