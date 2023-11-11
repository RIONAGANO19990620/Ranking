from django.shortcuts import render
from .models import NumberPlate
from django.db.models import Q
import re
from random import choice
from django.contrib.sessions.models import Session

from user_agents import parse
import random


def search_numberplate(request):
    user_agent = parse(request.META.get('HTTP_USER_AGENT'))
    query = request.GET.get('query', '')

    # 全部表示する時の入力
    if query == "all":
        numberplates = NumberPlate.objects.all().order_by('-value')

    # スペースを除いた全ての文字が数字の場合
    elif query and query.replace(" ", "")[0:].isdigit():
        q_objects = Q()  # 空のQオブジェクトを作成
        words = query.split()
        for keyword in words:
            q_objects |= Q(value=keyword)
        numberplates = NumberPlate.objects.filter(q_objects).order_by('-value')

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
            q_objects |= Q(value=i)
        numberplates = NumberPlate.objects.filter(q_objects).order_by('-value')

    elif query:
        q_objects = Q()
        words = query.split()
        clean_words = []

        for word in words:
            # 完全一致させたい場合は""ではさむ
            if word.startswith('"') or word.startswith('“') and word.endswith('"'):
                clean_words.append(word[1:-1])

        # 完全一致企業
        for clean_word in clean_words:
            q_objects |= Q(name__iexact=clean_word)

        # 部分一致企業
        lax_words = [x for x in words if x not in clean_words]
        for keyword in lax_words:
            q_objects |= Q(name__icontains=keyword)

            # -で単語除去
            if keyword.startswith('-'):
                keyword = keyword.replace("-", "")
                q_objects = q_objects & ~Q(name__icontains=keyword)

        numberplates = NumberPlate.objects.filter(q_objects).order_by('-value')  # 偏差値順に並び替えて検索
    else:
        numberplates = None

    context = {
        'user_agent': user_agent,
        'query': query,
        'numberplates': numberplates,
    }

    return render(request, 'numberplate_search.html', context)