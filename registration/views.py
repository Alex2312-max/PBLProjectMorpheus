from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


from .forms import SignUpForm, AccountAuthenticationForm


def registration_view(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/updatePage')
        else:
            context['signup_form'] = form
    else:
        form = SignUpForm()
        context['signup_form'] = form
    return render(request, 'registration/registration.html', context)


# Logout function
def logout_view(request):
    logout(request)
    return redirect('login')


# Login function
def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect(f'/userPage/{user.id - 1}')

    if request.method == "POST":
        form = AccountAuthenticationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user and user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('/adminPage')
            elif user:
                login(request, user)
                return redirect(f'/userPage/{user.id - 1}')

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'registration/loginPage.html', context)
