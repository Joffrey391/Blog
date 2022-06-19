from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.contrib.auth.models import User
from .forms import Post_Form, Post_Update_Form, Comment_Form, Password_Post_Form
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()
class create_post_view(CreateView):
    model = Post
    form_class = Post_Form
    template_name = 'create_post.html'

class update_post_view(UpdateView):
    model = Post
    form_class = Post_Update_Form
    template_name = 'update_post.html'
    # fields = '__all__'
    #fields = ['title','content','image']

class delete_post_view(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('my_blog')

def search_view(request):
    if request.method == "POST":
        searched = request.POST['searched']
        scan_post = Post.objects.filter(
            (Q(title__icontains=searched) |
            Q(user__username__icontains=searched) |
            Q(contents__icontains=searched)) &
            (Q(limit__icontains='P') | Q(limit__icontains='Pr'))
        )
        scan_post.distinct()
        return render(request, "search_result.html", {'searched': searched, 'scan_post': scan_post})
    else:
        return render(request, "search_result.html", {})

def the_blog_view(request):
    queryset = Post.objects.filter(Q(limit__icontains='P') | Q(limit__icontains='Pr'))
    context = {
        "object_list": queryset,
    }
    return render(request, "the_blog.html", context)

def post_lookup(request, id=id):
    take_post = Post.objects.get(id=id)
    take_coments = Comment.objects.all().filter(post=id)

    new_comment_form = Comment_Form()
    if request.method == "POST":
        new_comment_form = Comment_Form(request.POST)
        if new_comment_form.is_valid():
            contents = new_comment_form.cleaned_data.get('contents')
            post = take_post
            user = User.objects.get(id=new_comment_form.cleaned_data.get('user'))

            new_comment_create = Comment(contents=contents, post=post, user=user)
            new_comment_create.save()
        else:
            print(new_comment_form.errors)

    context = {
        "post":  take_post,
        "coments_list": take_coments,
        "form": new_comment_form,
    }
    return render(request, "post_detail.html", context)

def post_lookup_view(request, id=id):
    take_post = Post.objects.get(id=id)
    take_coments = Comment.objects.all().filter(post=id)

    if take_post.limit == "Pr":
        if request.session.get('password'):
            password = request.session.get('password')
            if password == take_post.password:
                return post_lookup(request, id=id)

        new_password_form = Password_Post_Form()
        if request.method == "POST":
            new_password_form = Password_Post_Form(request.POST)
            if new_password_form.is_valid():
                password = new_password_form.cleaned_data.get('password')

                if (password == take_post.password):
                    request.session['password'] = password
                    return redirect('post-detail', id=id)
            else:
                print(new_password_form.errors)

        context = {
            "post":  take_post,
            "coments_list": take_coments,
            "form": new_password_form,
        }
        return render(request, "password_post.html", context)
    else:
        return post_lookup(request, id=id)

def delete_password(request):
    try:
        del request.session['password']
    except KeyError:
        pass
    return HttpResponse("<h1>dataflair<br>Session Data cleared</h1>")

def my_blog_view(request):
    queryset = Post.objects.filter(Q(user__username__icontains=request.user.username))
    context = {
        "object_list": queryset,
    }
    return render(request, "my_blog.html", context)

def base_page_view(request):
    return render(request, "base.html", {})