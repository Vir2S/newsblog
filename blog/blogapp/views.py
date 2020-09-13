from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Post, Tag


def home(request):

    context = {
        'posts': Post.objects.all(),
        'tags': Tag.objects.all()
    }

    return render(request, 'blogapp/home.html', context)


class TagMixin(object):

    def get_context_data(self, **kwargs):

        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()

        return context


class PostListView(TagMixin, ListView):

    model = Post
    template_name = 'blogapp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


class UserPostListView(TagMixin, ListView):

    model = Post
    template_name = 'blogapp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(TagMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    fields = ['title', 'post_image', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    fields = ['title', 'post_image', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True

        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    success_url = '/'

    def test_func(self):

        post = self.get_object()

        if self.request.user == post.author:
            return True

        return False


class TagIndexView(TagMixin, ListView):

    model = Post
    template_name = 'blogapp/tag_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug'))

    def tag_posts(self, name):
        return Tag.objects.filter(tags__name=self.get('name'))


def about(request):
    return render(request, 'blogapp/about.html', {'title': 'About'})
