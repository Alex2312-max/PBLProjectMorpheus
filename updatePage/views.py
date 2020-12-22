from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UpdateInfoForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from updatePage.models import UpdatePage


def updatePage_view(request):
    if request.method == 'POST':
        form = UpdateInfoForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            user_id = len(UpdatePage.objects.all())
            return HttpResponseRedirect(f'/userPage/{user_id}')
    else:
        form = UpdateInfoForm()
    return render(request, 'updatePage/updatePage.html', {'form': form})

