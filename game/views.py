from django.shortcuts import render

def index(request):
    """ View function for index page """

    context = {
        'text' : 'Game here'
    }
    return render(request, 'index.html', context=context)