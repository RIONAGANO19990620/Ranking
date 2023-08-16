from django.shortcuts import render
from .models import HighSchool


def search_highschool(request):
    query = request.GET.get('query', '')  # Get the user input from the query parameter
    if query is '':
        high_schools = None

    elif query.isdigit():
        high_schools = HighSchool.objects.filter(value=int(query))
    else:
        high_schools = HighSchool.objects.filter(name__icontains=query)

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
