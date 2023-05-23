from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import CreatUserForm,LoginForm,CreateTaskForm,UpdateUserForm,UpdateProfileForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from . models import Task,Profile


# Create your views here.
def home(request):
    return render(request,'index.html')

def register(request):
    form = CreatUserForm()
    if request.method == 'POST':
        form = CreatUserForm(request.POST)

        if form.is_valid():
            current_user = form.save(commit = False)
            form.save()
            profile = Profile.objects.create(user=current_user)
            return HttpResponseRedirect('login')
    context = {'form':form}
    return render(request,'register.html',context)

def login(request):

    form = LoginForm

    if request.method == 'POST':
        form = LoginForm(request,data = request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('dashboard')
    context = {'form':form}
    return render(request,"login.html",context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url = 'login')
def dashboard(request):

    profile = Profile.objects.get(user=request.user)
    context = {'profile':profile}
    return render(request,'profile/dashboard.html',context = context)

def profile_management(request):

    user_form = UpdateUserForm(instance=request.user)
    profile = Profile.objects.get(user=request.user)
    form2 = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST,instance=request.user)

        form2 = UpdateProfileForm(request.POST,request.FILES,instance=profile)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect('dashboard')
        if form2.is_valid():
            form2.save()
            return HttpResponseRedirect('dashboard')
        
    
    
    context = {'userform':user_form,'form2':form2}
    return render(request,'profile/profile-management.html',context)

@login_required(login_url = 'login')
def createTask(request):
    form = CreateTaskForm

    if request.method == 'POST':

        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return HttpResponseRedirect('view-task')
    context = {'form':form}
    return render(request,'profile/create-task.html',context)

@login_required(login_url = 'login')
def viewTask(request):
    current_user =request.user.id
    task = Task.objects.all().filter(user = current_user)
    context = {'task':task}

    return render(request,'profile/view-task.html',context)

@login_required(login_url = 'login')
def updateTask(request,pk):
    task = Task.objects.get(id=pk)

    form = CreateTaskForm(instance=task)

    if request.method == 'POST':

        form  = CreateTaskForm(request.POST,instance=task)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/view-task')
        
    context = {'form':form}

    return render(request,'profile/update-task.html',context)

def deleteTask(request,pk):
    task = Task.objects.get(id = pk)
    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect('/view-task')
    return render(request,'profile/delete-task.html')
