from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from blogapp.models import BlogPost
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from .models import BlogPost, Comment, CommentLike
from .forms import CommentForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class SignupView(View):
    def get(self, request):
        return render(request, 'signup.html') 
    
    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Signup successful. You can now log in.')
                return redirect('/')
            except Exception as e:
                messages.error(request, 'Failed to signup')
                return redirect('signup')
        else:
            messages.error(request, 'Invalid request method')
            return redirect('signup')
        
 
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html') 
    
    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog-list')
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('login')

class CreateBlog(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'create_blog.html')

    def post(self, request):
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            if title and content: 
                blog = BlogPost.objects.create(title=title, content=content, author=request.user)
                messages.success(request, 'Blog post successfully created.')
                return redirect('create-blog') 
            else:
                messages.error(request, 'Title and content are required.')
        return redirect('create-blog')

    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') 
        return super().dispatch(request, *args, **kwargs)


class BlogListView(View):
    @method_decorator(login_required)
    def get(self, request):
        posts = BlogPost.objects.all()
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        try:
            page = paginator.get_page(page_number)
        except PageNotAnInteger:
            page = paginator.get_page(1)
        except EmptyPage:
            page = paginator.get_page(paginator.num_pages)
        return render(request, 'blog_list.html', {'page': page})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') 
        return super().dispatch(request, *args, **kwargs)


# from django.contrib.auth.mixins import LoginRequiredMixin

# class BlogListView(LoginRequiredMixin, View):
#     def get(self, request):
#         posts = BlogPost.objects.filter(author=request.user)
#         paginator = Paginator(posts, 5)
#         page_number = request.GET.get('page')
#         try:
#             page = paginator.get_page(page_number)
#         except PageNotAnInteger:
#             page = paginator.get_page(1)
#         except EmptyPage:
#             page = paginator.get_page(paginator.num_pages)
#         return render(request, 'blog_list.html', {'page': page})


class BlogDetailView(View):
    template_name = 'blog_detail.html'
    @method_decorator(login_required)
    def get(self, request, pk):
        blog_post = BlogPost.objects.get(pk=pk)
        comments = Comment.objects.filter(post=blog_post)
        comment_form = CommentForm()
        context = {
            'blog_post': blog_post,
            'comments': comments,
            'comment_form': comment_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        blog_post = BlogPost.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = blog_post
            new_comment.save()
        return redirect('blog_detail', pk=pk)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') 
        return super().dispatch(request, *args, **kwargs)

class CommentLikeView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        user = request.user
        like, created = CommentLike.objects.get_or_create(comment=comment, user=user)
        if not created:
            like.delete()
        return redirect('blog_detail', pk=comment.post.pk)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') 
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        blog_post = BlogPost.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog_post
            comment.user = request.user
            comment.save()
        return redirect('blog_detail', pk=pk)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') 
        return super().dispatch(request, *args, **kwargs)