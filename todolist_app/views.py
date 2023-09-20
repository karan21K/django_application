from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.forms import taskform
from todolist_app.models import tasklist
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
    if request.method == "POST":
        form = taskform(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request,("New Task Added!"))
        return redirect('todolist')
    else:    
        all_task = tasklist.objects.filter(manage=request.user)
        paginator = Paginator(all_task, 3)
        page = request.GET.get('pg')
        all_task = paginator.get_page(page)
        
        return render(request, 'todolist.html', {'all_task':all_task})

@login_required    
def delete_task(request,task_id):
    task = tasklist.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request,("Access Restricted, you are Not allowed"))
    return redirect('todolist')

@login_required
def edit_task(request,task_id):
    if request.method == "POST":
        task = tasklist.objects.get(pk=task_id)
        form =taskform(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request,("Task Edited"))
        return redirect('todolist')
    else:    
        task_obj = tasklist.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj':task_obj})
 
@login_required    
def complete_task(request,task_id):
    task = tasklist.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()  
    else:
        messages.error(request,("Access Restricted, you are Not allowed"))  
    return redirect('todolist')

@login_required
def pending_task(request,task_id):
    task = tasklist.objects.get(pk=task_id)
    task.done = False
    task.save()    
    return redirect('todolist')

def index(request):
    context = {
        'index_Text': "Welcome to index page"
        }
    return render(request, 'index.html', context)


def contact(request):
    context = {
        'contact_Text': "Welcome to contact page"
        }
    return render(request, 'contact.html', context)

def about(request):
    context = {
        'about_Text': "Welcome to about page"
        }
    return render(request, 'about.html', context)