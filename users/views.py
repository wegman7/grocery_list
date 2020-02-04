from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages

from .models import List

def home(request):
    context = {
        'items': List.objects.all(),
    }
    return render(request, 'users/home.html', context)

def login_view(request):
    context = {'message': 'Incorrect username or password'}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', context)
    else:
        return render(request, 'users/login.html')
    # if request.method == 'POST':
    #     form = AuthenticationForm(data=request.POST)
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         return redirect('home')
    # else:
    #     form = AuthenticationForm()
    # return render(request, 'users/login.html', {'message': 'Incorrect username or password'})

def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created!")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def list_view(request):
    context = {
        'items': List.objects.filter(user=request.user),
    }
    # if cancel button is pressed on page, page is reloaded
    if request.method == 'POST' and request.POST.get('cancel'):
        pass
    # item is added
    elif request.method == 'POST' and request.POST.get('added-text') is not None:
        new_list_item = request.POST.get('added-text')
        if len(new_list_item) > 0:
            new_list_item = List(item=new_list_item, user=request.user)
            new_list_item.save()
        else:
            messages.error(request, "Invalid item")
    # item(s) are deleted
    else:
        delete_list = []
        for item in List.objects.all():
            if request.POST.get(item.item) is not None:
                delete_list.append(item.item)
                List.objects.filter(item=item.item).delete()
    return render(request, 'users/list_view.html', context)
