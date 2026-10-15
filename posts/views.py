from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from account.models import Profile
from .models import Post
from .forms import PostForm, CommentForm

@login_required
def dashboard(request):
    mine, _ = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.select_related('user', 'user__profile').prefetch_related('likes', 'comments__user').order_by('-created_at', '-pk')
    q = request.GET.get('q', '').strip()
    if q:
        posts = posts.filter(Q(content__icontains=q) | Q(user__username__icontains=q))
    if request.GET.get('feed') == 'following':
        posts = posts.filter(Q(user=request.user) | Q(user__profile__in=mine.following.all()))
    page = Paginator(posts, 10).get_page(request.GET.get('page'))
    return render(request, 'dashboard.html', {'posts': page, 'page_obj': page, 'form': PostForm(), 'mine': mine, 'q': q})

@login_required
def upload_files(request):
    if request.method != 'POST':
        return redirect('dashboard')
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Post published.')
        return redirect('dashboard')
    return render(request, 'form.html', {'form': form, 'heading': 'Create a post'}, status=400)

@login_required
def edit(request, id):
    post = get_object_or_404(Post, id=id, user=request.user)
    form = PostForm(request.POST if request.method == 'POST' else None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Post updated.')
        return redirect('dashboard')
    return render(request, 'form.html', {'form': form, 'heading': 'Edit post'})

@login_required
@require_POST
def remove_post(request, id):
    get_object_or_404(Post, id=id, user=request.user).delete()
    messages.success(request, 'Post deleted.')
    return redirect('dashboard')

@login_required
@require_POST
def like(request, id):
    post = get_object_or_404(Post, id=id)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('dashboard')

@login_required
@require_POST
def comment(request, id):
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.post, item.user = post, request.user
        item.save()
    else:
        messages.error(request, 'Comments must contain between 1 and 1,000 characters.')
    return redirect('dashboard')
