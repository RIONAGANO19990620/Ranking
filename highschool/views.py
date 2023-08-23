from django.shortcuts import render
from .models import HighSchool
from django.db.models import Q


def search_highschool(request):
    query = request.GET.get('query', '')  # Get the user input from the query parameter

    if query.isdigit():
        high_schools = HighSchool.objects.filter(value=int(query))

    elif query:
        keywords = query.split()  # クエリを空白で分割してキーワードのリストを作成
        q_objects = Q()  # 空のQオブジェクトを作成

        for keyword in keywords:
            q_objects |= Q(name__icontains=keyword)  # 各キーワードに対してQオブジェクトを結合

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
