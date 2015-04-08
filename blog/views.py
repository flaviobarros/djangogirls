import django.shortcuts
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm


def post_list(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return django.shortcuts.render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = django.shortcuts.get_object_or_404(Post, pk=pk)
    return django.shortcuts.render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):

    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return django.shortcuts.redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()

    return django.shortcuts.render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):

    post = django.shortcuts.get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return django.shortcuts.redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return django.shortcuts.render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return django.shortcuts.render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = django.shortcuts.get_object_or_404(Post, pk=pk)
    post.publish()
    return django.shortcuts.redirect('blog.views.post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = django.shortcuts.get_object_or_404(Post, pk=pk)
    post.delete()
    return django.shortcuts.redirect('blog.views.post_list')
