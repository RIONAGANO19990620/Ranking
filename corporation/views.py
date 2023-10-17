from django.shortcuts import render
from .models import Corporation
from django.db.models import Q
import re
from random import choice
from django.contrib.sessions.models import Session

from user_agents import parse


def search_corporation(request):
    user_agent = parse(request.META.get('HTTP_USER_AGENT'))
    query = request.GET.get('query', '')  # Get the user input from the query parameter

    if query == "all":
        corporations = Corporation.objects.all().order_by('-value')

    elif query and query.replace(" ", "")[0:].isdigit():  # スペースを除いた全ての文字が数字の場合

        q_objects = Q()  # 空のQオブジェクトを作成
        words = query.split()
        for keyword in words:
            q_objects |= Q(value=keyword)
        corporations = Corporation.objects.filter(q_objects).order_by('-value')

    elif query and "~" in query:  # 範囲検索
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
        corporations = Corporation.objects.filter(q_objects).order_by('-value')

    elif query:
        q_objects = Q()  # 空のQオブジェクトを作成
        words = query.split()  # クエリを空白で分割してキーワードのリストを作成
        clean_words = []

        for word in words:
            if word.startswith('"') or word.startswith('“') and word.endswith('"'):  # 完全一致させたい場合は""ではさむ
                clean_words.append(word[1:-1])

        for clean_word in clean_words:
            q_objects |= Q(name__iexact=clean_word)  # 完全一致企業

        lax_words = [x for x in words if x not in clean_words]
        for keyword in lax_words:
            q_objects |= Q(name__icontains=keyword)  # 部分一致企業

            if keyword.startswith('-'):
                keyword = keyword.replace("-", "")
                q_objects = q_objects & ~Q(name__icontains=keyword)  # -で単語除去

        corporations = Corporation.objects.filter(q_objects).order_by('-value')  # 偏差値順に並び替えて検索
    else:
        corporations = None

    context = {
        'user_agent': user_agent,
        'query': query,
        'corporations': corporations,
    }

    return render(request, 'corporation_search.html', context)


def quiz_corporation(request):
    # セッションから前回のcorporationを取得
    random_corporation = request.session.get("random_corporation")

    # セッションにランダムなcorporationがない場合は新たに生成
    if not random_corporation:
        random_corporation = choice(Corporation.objects.all())
        request.session["random_corporation"] = random_corporation

    result_message = ""
    answer = ""
    guess = None

    if request.method == "POST":
        guess = int(request.POST["guess"])
        answer = "正解：" + str(random_corporation.value)

        if guess == random_corporation.value:
            result_message = "あたり😆"
        elif guess >= random_corporation.value + 5:
            result_message = "そんな高くないで😫"
        elif guess <= random_corporation.value - 5:
            result_message = "見くびりすぎなんちゃう😵"
        else:
            result_message = "さげ😅"

        # 新しいランダムな企業をセッションに保存
        random_corporation = choice(Corporation.objects.all())
        request.session["random_corporation"] = random_corporation
        request.session.save()  # セッションを保存

    context = {
        'corporation': random_corporation,
        'result': result_message,
        'guess': guess,
        'answer': answer,
    }

    return render(request, 'corporation_quiz.html', context)
