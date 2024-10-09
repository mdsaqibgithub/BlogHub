from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.views import View

from .forms import RegisterForm, LoginForm, CommentForm
from .models import Blog, Comment


# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        msg = None
        if form.is_valid():
            form.save()
            return redirect('login-page')
        else:
            return render(request, 'register.html', {'form': form, 'msg':msg})


class LoginView(View):
    def get(self, request):
        form = LoginForm(request.POST or None)
        msg = None
        return render(request, 'login.html', {'form': form, 'msg': msg})
    
    def post(self, request):
        form = LoginForm(request.POST)
        msg = None
        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('blog_list')
                else:
                    msg = 'Invalid Credentials'
            else:
                msg = 'Error Validating Form'
        return render(request, 'login.html', {'form': form, 'msg':msg})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login-page')
    
    def post(self, request):
        logout(request)
        return redirect('login-page')


@login_required
def blog_list(request):
    blogs = Blog.objects.exclude(slug__isnull=True).exclude(slug__exact='')  # Exclude blogs with empty slugs
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog_list.html', {'page_obj': page_obj})

@login_required
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments = blog.comments.all()
    return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments})

def like_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)

    return redirect('blog_detail', slug=blog.slug)


@login_required
def add_comment(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('blog_detail', slug=slug)
    return redirect('blog_detail', slug=slug)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('blog_detail', slug=comment.blog.slug)

