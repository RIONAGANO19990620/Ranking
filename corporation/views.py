from django.shortcuts import render
from .models import Corporation


def search_corporation(request):
    query = request.GET.get('query', '')  # Get the user input from the query parameter
    if query is '':
        corporations = None

    elif query.isdigit():
        corporations = Corporation.objects.filter(value=int(query))
    else:
        corporations = Corporation.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'corporations': corporations,
    }

    return render(request, 'corporation_search.html', context)
