from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.

from . models import User
from . forms import UserForm

def index(request):
    return render(request, 'index.html')

def showUserDetail(request, pk):
    user = get_object_or_404(User, id=pk)
    context = {'user': user}

    return render(request, 'home/user_detail.html', context)

def updateUser(request, pk):
    user = get_object_or_404(User, id=pk)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user', pk=pk) 
        
    context = {'form': form}

    return render(request, 'home/user_update.html', context)

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/register.html', { 'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, _('You have singed up successfully.'))
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/register.html', {'form': form})

