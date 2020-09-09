from django.shortcuts import render

posts = [
    {
        'author': 'Vitaly Sem',
        'title': 'Blog post 1',
        'content': 'Post 1 content',
        'date_posted': 'September 09, 2020',
    },
    {
        'author': 'Vitaly Sem',
        'title': 'Blog post 2',
        'content': 'Post 2 content',
        'date_posted': 'September 09, 2020',
    }
]


def home(request):

    context = {
        'posts': posts,
    }

    return render(request, 'blogapp/home.html', context=context)


def about(request):
    return render(request, 'blogapp/about.html', context={'title': 'About'})
