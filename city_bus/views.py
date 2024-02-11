from django.shortcuts import render
from .models import CityBus
from django.db.models import Q
import re
from random import choice
from django.contrib.sessions.models import Session

from user_agents import parse
import random


def search_city_bus(request):
    user_agent = parse(request.META.get('HTTP_USER_AGENT'))
    query = request.GET.get('query', '')

    # 全部表示する時の入力
    if query == "all":
        city_buses = CityBus.objects.all().order_by('sale__sale')

    # スペースを除いた全ての文字が数字の場合
    elif query and query.replace(" ", "")[0:].isdigit():
        q_objects = Q()  # 空のQオブジェクトを作成
        words = query.split()
        for keyword in words:
            q_objects |= Q(sale__sale=keyword)
            q_objects |= Q(number=keyword)
        city_buses = CityBus.objects.filter(q_objects)

    # 範囲検索
    elif query and "~" in query:
        match = re.match(r"(\d+)~(\d+)", query)

        if int(match.group(1)) < int(match.group(2)):
            from_value = int(match.group(1))
            to_value = int(match.group(2))
        else:
            from_value = int(match.group(2))
            to_value = int(match.group(1))

        q_objects = Q()
        for i in range(from_value, to_value + 1):
            q_objects |= Q(sale__sale=i)
        city_buses = CityBus.objects.filter(q_objects).order_by('sale__sale')

    else:
        city_buses = None

    context = {
        'user_agent': user_agent,
        'query': query,
        'city_bus': city_buses,
    }

    return render(request, 'city_bus_search.html', context)
