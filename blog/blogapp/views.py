from django.shortcuts import render
from .models import Post


def home(request):

    context = {
        'posts': Post.objects.all(),
    }

    return render(request, 'blogapp/home.html', context=context)


def about(request):
    return render(request, 'blogapp/about.html', context={'title': 'About'})
