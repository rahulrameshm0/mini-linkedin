from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post

# Create your views here.

@login_required(login_url="signin")
def dashboard(request):
    if request.method == "POST":
        print("POST HIT")
        print("CONTENT:", request.POST.get("content"))
        print("FILES:", request.FILES)

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
