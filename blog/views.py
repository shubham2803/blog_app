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

# from django.views.generic
from .models import Post

# Create your views here.
posts = [
    {'title': 'Blog Post 1',
     'author': 'Sample Author 1',
     'date': 'Aug 21, 2019',
     'content': 'This is content in the first blog'},
    {'title': 'Blog Post 2',
     'author': 'Sample Author 2',
     'date': 'Aug 23, 2019',
     'content': 'This is content in the second blog'}
]


def homePage(request):
    posts = Post.objects.all()
    context = {
        'title': 'Home',
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

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


def aboutPage(request):
    context = {}
    return render(request, 'blog/about.html', )
