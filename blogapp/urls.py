from django.urls import path
from blogapp.views import SignupView, LoginView, CreateBlog, BlogListView, BlogDetailView, CommentCreateView, CommentLikeView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', LoginView.as_view(), name='login'),
    path('create-blog', CreateBlog.as_view(), name='create-blog'),
    path('blog-list', BlogListView.as_view(), name='blog-list'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('comment/create/<int:pk>/', CommentCreateView.as_view(), name='comment_create'),
    path('like_comment/<int:pk>/', CommentLikeView.as_view(), name='like_comment'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
