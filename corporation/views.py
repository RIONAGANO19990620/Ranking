from django.shortcuts import render
from .models import Corporation
from django.db.models import Q


def search_corporation(request):
    query = request.GET.get('query', '')  # Get the user input from the query parameter

    if query.isdigit():
        corporations = Corporation.objects.filter(value=int(query))

    elif query:
        keywords = query.split()  # クエリを空白で分割してキーワードのリストを作成
        q_objects = Q()  # 空のQオブジェクトを作成

        for keyword in keywords:
            q_objects |= Q(name__icontains=keyword)  # 各キーワードに対してQオブジェクトを結合

        corporations = Corporation.objects.filter(q_objects)
    else:
        corporations = None

    context = {
        'query': query,
        'corporations': corporations,
    }

    return render(request, 'corporation_search.html', context)

