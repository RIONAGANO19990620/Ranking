from django.shortcuts import render
from .models import Corporation, QuizHistory
from django.db.models import Q
import re
from random import choice
from django.contrib.sessions.models import Session

from user_agents import parse
import random


def search_corporation(request):
    user_agent = parse(request.META.get('HTTP_USER_AGENT'))
    query = request.GET.get('query', '')

    # 全部表示する時の入力
    if query == "all":
        corporations = Corporation.objects.all().order_by('-value')

    # スペースを除いた全ての文字が数字の場合
    elif query and query.replace(" ", "")[0:].isdigit():
        q_objects = Q()  # 空のQオブジェクトを作成
        words = query.split()
        for keyword in words:
            q_objects |= Q(value=keyword)
        corporations = Corporation.objects.filter(q_objects).order_by('-value')

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
        corporations = Corporation.objects.filter(q_objects).order_by('-value')

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
    result_message = ""
    answer = ""
    guess = None
    quiz_history = ""
    selectable_list = [i for i in range(55, 82)]
    latest_quiz_history = None

    user_agent = parse(request.META.get('HTTP_USER_AGENT'))
    # セッションから前回のcorporationを取得
    random_corporation = request.session.get("random_corporation")

    # セッションにランダムなcorporationがある場合は選択肢を作る
    if random_corporation:
        selectable_list.remove(random_corporation.value)
        choices = sorted(random.sample(selectable_list, 5) + [random_corporation.value])

    # セッションにランダムなcorporationがない場合は新たに生成
    else:
        random_corporation = choice(Corporation.objects.all())
        request.session["random_corporation"] = random_corporation
        selectable_list.remove(random_corporation.value)
        choices = sorted(random.sample(selectable_list, 5) + [random_corporation.value])

    # 解答と比較
    if request.method == "POST":
        guess = int(request.POST["guess"])
        answer = "正解：" + str(random_corporation.value)

        if guess == random_corporation.value:
            result_message = "あたり😆"
            is_correct = True
        elif guess >= random_corporation.value + 5:
            result_message = "そんな高くないで😫"
            is_correct = False
        elif guess <= random_corporation.value - 5:
            result_message = "見くびりすぎなんちゃう😵"
            is_correct = False
        else:
            result_message = "さげ😅"
            is_correct = False

        # クイズの出題履歴をデータベースに保存
        quiz_history = QuizHistory(
            question=random_corporation.name,
            answer=str(random_corporation.value),
            user_answer=str(guess),
            is_correct=is_correct
        )

        quiz_history.save()

        # 新しいランダムな企業をセッションに保存
        random_corporation = choice(Corporation.objects.all())
        request.session["random_corporation"] = random_corporation
        request.session.save()  # セッションを保存
        selectable_list = [i for i in range(55, 81)]
        selectable_list.remove(random_corporation.value)
        choices = sorted(random.sample(selectable_list, 5) + [random_corporation.value])
        quiz_history = QuizHistory.objects.order_by('-created_at')[:10]
        latest_quiz_history = QuizHistory.objects.order_by('-created_at').first()

    context = {
        'user_agent': user_agent,
        'corporation': random_corporation,
        'result': result_message,
        'guess': guess,
        'answer': answer,
        'choices': choices,
        'quiz_history': quiz_history,
        'latest_quiz_history': latest_quiz_history,
    }

    return render(request, 'corporation_quiz.html', context)
