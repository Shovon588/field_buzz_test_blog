from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView
from django.http import JsonResponse, HttpResponse
import json

from .forms import SignupForm, NewPostForm, CommentForm
from .models import Blog, ReaderInfo, Comment


# Create your views here.


def home(request):
    post_list = Blog.objects.filter(published=True).order_by('-created_at')
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Blog/home.html', context={'page_obj': page_obj})


def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            user = form.save()
            user.set_password(password)
            user.save()
            return redirect("login")
        else:
            messages.error(request, message=form.errors)

    return render(request, 'registration/signup.html', context={"form": form})


@login_required
def new_post(request):
    form = NewPostForm()
    if request.method == "POST":
        user = request.user
        title = request.POST['title']
        post = request.POST['post']
        Blog.objects.create(user=user, title=title, post=post)
        messages.success(request, message="New post created")
        return redirect("my-post")

    return render(request, 'Blog/new_post.html', context={'form': form})


@login_required
def my_post(request):
    post_list = Blog.objects.filter(user=request.user, created_at__lte=timezone.now()).order_by('-created_at')
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Blog/my_post.html', context={'page_obj': page_obj})


def post_detail(request, slug):
    post = Blog.objects.get(slug=slug)
    form = CommentForm()
    if request.user != post.user:
        readerinfo = ReaderInfo(post=post)
        readerinfo.save()

    return render(request, 'Blog/post_detail.html', context={'post': post, 'form': form})


def approved_comments(request, slug):
    post = Blog.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post, approved=True)
    comment_list = []

    for comment in comments:
        comment_list.append({comment.name: comment.comment})
    print(comment_list)

    return JsonResponse({"data": comment_list})


@login_required
def publish_post(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    post.published = True
    post.save()
    messages.success(request, message="Post Published!")
    return redirect("post-detail", slug=slug)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('my-post')


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        post.title = title
        post.post = text
        post.save()
        messages.success(request, message="Successfully updated!")
        return redirect('post-detail', slug=slug)

    return render(request, 'Blog/post_edit.html', context={'post': post})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.user.username != username:
        post_list = Blog.objects.filter(user=user, published=True, created_at__lte=timezone.now()).order_by(
            '-created_at')
        is_self = False
    else:
        post_list = Blog.objects.filter(user=user, created_at__lte=timezone.now()).order_by('-created_at')
        is_self = True

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "Blog/user_profile.html", context={"author": user, "page_obj": page_obj, "is_self": is_self})


def add_comment(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    if request.method == "POST":
        name = request.POST['name']
        comment = request.POST['comment']
        Comment.objects.create(post=post, name=name, comment=comment)
        messages.success(request, message="Comment will be added upon approval.")
        return redirect('post-detail', slug=slug)


@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approved = True
    comment.save()
    messages.success(request, message="Comment Approved")

    return redirect("post-detail", slug=comment.post.slug)


@login_required
def remove_comment(request, pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        messages.success(request, message="Comment Deleted")
        return redirect("post-detail", slug=comment.post.slug)

    return render(request, 'Blog/comment_confirm_delete.html')
