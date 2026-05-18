from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post


# Create your views here.
def dashboard(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "dashboard.html", {'posts':posts})

@login_required(login_url="signin")
def upload_files(request):
    
    if request.method == "POST":
        image = request.FILES.get("image")
        content = request.POST.get("content")

        Post.objects.create(
            user=request.user,
            content=content,
            image=image
        )

        return redirect("dashboard")
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "dashboard.html", {'posts':posts})


def edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        image = request.FILES.get("image")
        content = request.POST.get("content")
        # user = request.POST.get("user")

        post.content = content

        if image:
            post.image = image
        post.save()
        return redirect('dashboard')
    
    return render(request, "edit-posts.html", {"edit_posts":post})

def remove_post(request, id):
    delete_post = Post.objects.filter(id=id)
    delete_post.delete()
    return redirect('dashboard')