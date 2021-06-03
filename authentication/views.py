from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import NewUserForm

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                dj_login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                if user.is_superuser or user.is_staff:
                    return redirect('quiz/')
                return redirect('quiz/dashboard')

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    elif request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            print(True)
            return redirect('quiz/')
        return redirect('quiz/dashboard')

    form = AuthenticationForm()
    return render(request=request, template_name="login.html",
                  context={"form": form})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            dj_login(request, user)
            return redirect('login/')

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="register.html",
                          context={"form": form})

    form = NewUserForm()
    return render(request=request,
                  template_name="register.html",
                  context={"form": form})
