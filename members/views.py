from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from members.forms import RegistrationForm,LoginForm,AccountUpdateForm

def registration_view(request):
    context={}
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email=form.cleaned_data.get('email')
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(email=email,password=raw_password)
            login(request,user)
            return redirect('my_blog')
        else:
            context['registration_form']=form
    else:
        form=RegistrationForm()
        context['registration_form']=form
    return render(request,'registration/register.html',context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_user(request):
    context={}
    user=request.user
    if user.is_authenticated:
        return redirect('my_blog')

    if request.POST:
        form=LoginForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            raw_password=request.POST['password']
            user=authenticate(email=email,password=raw_password)
            if user:
                login(request,user)
                return redirect('my_blog')
    else:
        form=LoginForm()
    context['login_form']=form
    return render(request,'registration/login.html',context)

def account_view(request):
    if not request.user.is_authenticated:
        return render(request,'registration/login.html',{})
    context={}
    if request.POST:
        form=AccountUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form=AccountUpdateForm(
            initial={
                "email":request.user.email,
                "username":request.user.username,
                "first_name":request.user.first_name,
                "last_name":request.user.last_name,

            }
        )
    context['account_form']=form
    return render(request,'registration/account.html',context)
