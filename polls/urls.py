from django.urls import path
from polls.views import base_page_view, create_post_view, post_lookup_view, the_blog_view, my_blog_view, update_post_view, delete_post_view, search_view, delete_password

urlpatterns = [
    path('base', base_page_view),
    path('', the_blog_view, name='home'),

    path('post', create_post_view.as_view(), name='add_post'),
    path('posts/<int:id>', post_lookup_view, name='post-detail'),
    path('post/edit/<int:pk>', update_post_view.as_view(), name='edit_post'),
    path('post/remove/<int:pk>', delete_post_view.as_view(), name='delete_post'),
    path('post/searchResult', search_view, name='search'),
    path('delete/', delete_password),
    path('myBlog', my_blog_view, name='my_blog'),
]