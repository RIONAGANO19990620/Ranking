from django.shortcuts import render
from .models import University
from django.db.models import Q
import re
from user_agents import parse
from random import choice


def search_university(request):
    user_agent = parse(request.META.get('HTTP_USER_AGENT'))
    query = request.GET.get('query', '')  # Get the user input from the query parameter

    if query=="all":
        universities = University.objects.all()

    elif re.match(r'^[a-zA-Z]', query):
        universities = University.objects.filter(rank__icontains=query)

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

        universities = University.objects.filter(q_objects)
    else:
        universities = None

    context = {
        'user_agent': user_agent,
        'query': query,
        'universities': universities,
    }

    return render(request, 'university_search.html', context)


def quiz_university(request):
    # セッションから前回のuniversityを取得
    random_university = request.session.get("random_university")

    # セッションにランダムなuniversityがない場合は新たに生成
    if not random_university:
        random_university = choice(University.objects.all())
        request.session["random_university"] = random_university

    result_message = ""
    answer = ""
    guess = None

    if request.method == "POST":
        guess = str(request.POST["guess"])
        answer = "正解：" + random_university.rank

        if guess == random_university.rank:
            result_message = "あたり😆"
        # 新しいランダムな企業をセッションに保存
        random_university = choice(University.objects.all())
        request.session["random_university"] = random_university
        request.session.save()  # セッションを保存

        if result_message != "あたり😆":
            result_message = "さげ😅"

    context = {
        'university': random_university,
        'result': result_message,
        'guess': guess,
        'answer': answer
    }

    return render(request, 'university_quiz.html', context)

