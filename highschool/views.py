from django.shortcuts import render
from .models import HighSchool
from django.db.models import Q


def search_highschool(request):
    query = request.GET.get('query', '')  # Get the user input from the query parameter

    if query.isdigit():
        high_schools = HighSchool.objects.filter(value=int(query))

    elif query:
        words = query.split()  # クエリを空白で分割してキーワードのリストを作成
        q_objects = Q()  # 空のQオブジェクトを作成
        clean_words = []

        for word in words:
            if word.startswith('"') or word.startswith('“') and word.endswith('"'):  # 完全一致させたい場合は""ではさむ
                clean_words.append(word[1:-1])

        for clean_word in clean_words:
            q_objects |= Q(name__iexact=clean_word)  # 完全一致高校

        lax_words = [x for x in words if x not in clean_words]
        for keyword in lax_words:
            q_objects |= Q(name__icontains=keyword)  # 部分一致高校

            if keyword.startswith("-"):
                keyword = keyword.replace("-", "")
                q_objects = q_objects & ~Q(name__icontains=keyword)  # -で単語除去

        high_schools = HighSchool.objects.filter(q_objects).order_by('-value')

    else:
        high_schools = None

    if high_schools is not None:
        __high_schools = []
        names = []
        for high_school in high_schools:
            if high_school.name not in names:
                __high_schools.append(high_school)
            names.append(high_school.name)
        high_schools = __high_schools

    context = {
        'query': query,
        'high_schools': high_schools,
    }

    return render(request, 'high_school_search.html', context)
