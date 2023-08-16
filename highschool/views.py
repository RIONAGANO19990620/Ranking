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

    context = {
        'query': query,
        'high_schools': high_schools,
    }

    return render(request, 'high_school_search.html', context)
