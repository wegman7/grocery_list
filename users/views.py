from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
import json

from .models import List, ListItem, Profile, FriendRequest

def home(request):
    return render(request, 'users/home.html')

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

# def list_item_view(request):
    

@login_required
def list_view(request):
    lists = List.objects.filter(user=request.user)
    context = {
        'lists': lists
    }

    # if cancel button is pressed on page, page is reloaded
    if request.method == 'POST' and request.POST.get('cancel'):
        pass
    # list is added
    elif request.method == 'POST' and request.POST.get('added-text') is not None:
        new_list = request.POST.get('added-text')
        if len(new_list) > 0:
            new_list = List(list_name=new_list, user=request.user)
            new_list.save()
        else:
            messages.error(request, "Invalid list")
    # item(s) are deleted
    elif request.method == 'POST':
        for list_object in List.objects.all():
            if request.POST.get(list_object.list_name) is not None:
                List.objects.filter(list_name=list_object.list_name).delete()
        return redirect('list')
    return render(request, 'users/list_view.html', context)

@login_required
def item_view(request, pk):
    my_list = List.objects.get(pk=pk)
    items = ListItem.objects.filter(from_list=my_list)
    context = {
        'items': items
    }

    # if cancel button is pressed on page, page is reloaded
    if request.method == 'POST' and request.POST.get('cancel'):
        pass
    # item is added
    elif request.method == 'POST' and request.POST.get('added-text') is not None:
        new_list_item = request.POST.get('added-text')
        if len(new_list_item) > 0:
            new_list_item = ListItem(item=new_list_item, from_list=my_list)
            new_list_item.save()
        else:
            messages.error(request, "Invalid item")
    # item(s) are deleted
    elif request.method == 'POST':
        for item in items:
            if request.POST.get(item.item) is not None:
                ListItem.objects.filter(item=item.item).delete()
        return redirect(request.path_info)
    return render(request, 'users/item_view.html', context)

    """
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
        print(request.POST)
        delete_list = []
        for item in List.objects.all():
            if request.POST.get(item.item) is not None:
                delete_list.append(item.item)
                List.objects.filter(item=item.item).delete()
    return render(request, 'users/list_view.html', context)
    """

@login_required
def manage_friends(request):
    print('request inside manage_friends: ', request)
    if request.is_ajax():
        print("ajax !")

    profile = Profile.objects.get(user=request.user)
    friends = profile.friend.filter(friend=profile)

    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_sent = FriendRequest.objects.filter(from_user=request.user)

    context = {
        'friends': friends,
        'friend_requests': friend_requests,
        'friend_requests_sent': friend_requests_sent
    }

    # if cancel button is pressed on page, page is reloaded
    if request.method == 'POST' and request.POST.get('cancel'):
        pass
    # if friend request is added
    elif request.method == 'POST' and request.POST.get('added-text') is not None:
        print(request.POST)
        added_text = request.POST.get('added-text')
        print(len(added_text))
        if len(added_text) > 0 and len(User.objects.filter(username=added_text)) > 0 and added_text != request.user.username:
            if len(FriendRequest.objects.filter(from_user=request.user, to_user=User.objects.get(username=added_text))) == 0:
                new_friend_request = FriendRequest(from_user=request.user, to_user=User.objects.get(username=added_text))
                new_friend_request.save()
            else:
                messages.error(request, "Friend request already sent.")
        else:
            messages.error(request, "Invalid username.")
    # friend(s) are deleted
    elif request.method == 'POST':
        print(request.POST)
        for friend in friends:
            if request.POST.get(friend.user.username) is not None:
                profile.friend.remove(friend)
        # for some reason I have to return redirect to friends page for page to update friends list
        return redirect('friends')
    return render(request, 'users/manage_friends.html', context)

def add_friend_request(request):
    print("request inside add_friend: ", request)
    print(request.POST)

    if request.method == 'POST':
        # grab the username of profile we want to accept
        accept_user = request.POST.get('accept_user')
        # create instance my MY profile
        profile = Profile.objects.get(user=request.user)
        # create instance for profile we are accepting
        new_friend_profile = Profile.objects.get(user=User.objects.get(username=accept_user))

        profile.friend.add(new_friend_profile)

        # after adding the friend to our profile friends list, we need to delete the request by first creating an instance of it
        friend_request = FriendRequest.objects.get(from_user=User.objects.get(username=accept_user), to_user=request.user)
        friend_request.delete()

        # do this to refresh page
        print("return redirect goddamnit!")
        return redirect('/')
    
    print("and again return redirect goddamnit!")
    return redirect('home')

    context = {
        'users': User.objects.all()
    }
    return HttpResponse(context)

def remove_friend_request(request):
    print("request inside add_friend: ", request)
    print(request.POST)

    if request.method == 'POST':
        # grab name of user whose request we want to remove
        remove_user = request.POST.get('remove_user')
        # create instance of FriendRequest we want to delete
        friend_request = FriendRequest.objects.get(from_user=User.objects.get(username=remove_user), to_user=request.user)
        friend_request.delete()

        # do this to refresh page
        print("return redirect goddamnit!")
        return redirect('home')
    
    print("and again return redirect goddamnit!")
    return redirect('home')
    context = {
        'users': User.objects.all()
    }
    return HttpResponse(context)