from django.shortcuts import render,redirect,HttpResponse
from datetime import date
from time import *
from . models import *
# Create your views here.
def index(request):
    return render(request, 'main/index.html')
def createuser(request):
    did_create = User.objects.createuser(request)
    if did_create:
        return redirect('/')
    else:
        return redirect('/')
def login(request):
    did_login = User.objects.login(request)
    if did_login:
        return redirect('/user_dashboard')
    else:
        return redirect('/')

def user_dashboard(request):
    if 'logged_in'in request.session:
        user=User.objects.get(id=request.session['logged_in'])
        context = {
            "user":user,
            "today":date.today(),
            "tasks":Appointment.objects.filter(user__id=request.session['logged_in']).filter(date=date.today()),
            "other":Appointment.objects.filter(user__id=request.session['logged_in']).filter(date__gt=date.today()),
        }
        return render(request, 'main/user_dashboard.html', context)
    else:
        return redirect('/')

def task_delete(request, id):
    remove_task=Appointment.objects.filter(id=id)
    remove_task.delete()
    return redirect('/user_dashboard')

def add_appointment(request):
    new_app = Appointment.objects.createapp(request)
    if new_app:
        return redirect('/user_dashboard')
    else:
        return redirect('/user_dashboard')

def show_app(request, id):
    context = {
        "app":Appointment.objects.filter(id=id),
    }
    return render(request, 'main/show_app.html', context)

def edit_app(request, id):
    update_app = Appointment.objects.editapp(request)
    if update_app:
        return redirect('/user_dashboard')
    else:
        return redirect('/user_dashboard')
def logout(request):
    try:
        del request.session['logged_in']
    except KeyError:
        pass
    return HttpResponse("You're successfully logged out.")
    return redirect('/')
