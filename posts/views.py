from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .models import Post, Author, Subscription, Category
from .forms import PostForm
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 1


class PostSearch(ListView):
    model = Post
    ordering = 'created_at'
    template_name = 'posts/posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'posts/post_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('posts.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'posts/post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('posts.delete_post',)
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts:posts_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'posts/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )