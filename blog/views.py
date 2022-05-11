from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from .forms import NewUserForm, PostForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registracija sėkminga.")
            return redirect("home")
        messages.error(request, "Registracija nesėkmynga.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Jūs prisijungėte kaip {username}.")
                return redirect("home")
            else:
                messages.error(request, "Neteisingai įvestas vartotojas arba slaptažodis.")
        else:
            messages.error(request, "Neteisingai įvestas vartotojas arba slaptažodis.")
    form = CustomAuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def add_post(request):
    context = {}

    if not request.user.is_authenticated:
        return redirect('login')

    form = PostForm(request.POST or None)
    form.fields['author'].initial = request.user
    form.fields['author'].widget = forms.HiddenInput()

    if form.is_valid():
        form.save()
        return redirect('home')

    context['form'] = form
    return render(request, "post.html", context)
