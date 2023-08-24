from django.shortcuts import render
from .models import Corporation
from django.db.models import Q


def search_corporation(request):
    query = request.GET.get('query', '')  # Get the user input from the query parameter

    if query.isdigit():
        corporations = Corporation.objects.filter(value=int(query))

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
        'query': query,
        'corporations': corporations,
    }

    return render(request, 'corporation_search.html', context)

