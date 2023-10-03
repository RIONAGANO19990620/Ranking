from django.shortcuts import render
from .models import University
from django.db.models import Q
import re
from user_agents import parse


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

