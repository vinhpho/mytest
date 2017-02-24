from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from datetime import datetime
from time import *
import bcrypt


class UserManager(models.Manager):
    def createuser(self,request):
        is_valid = True
        if len(request.POST['name']) == 0:
            is_valid = False
            messages.error(request,'First Name is required.')
        if len(request.POST['bday'])== 0:
            is_valid = False
            messages.error(request,'Birthday is required.')
        if len(request.POST['email']) == 0:
            is_valid = False
            messages.error(request,'Email is required.')
        email_check = User.objects.filter(email=request.POST['email'])
        if len(email_check) > 0:
            is_valid= False
            messages.error(request, 'Email is already exist')
        if len(request.POST['password'])< 8:
            is_valid = False
            messages.error(request, 'Password requires at least 8 characters')
        if request.POST['password'] != request.POST['confirm_password']:
            messages.error(request, 'Password and confirm password do not match')
            is_valid = False
        if not is_valid:
            return is_valid
        hashed = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User(
            name=request.POST['name'],
            bday = request.POST['bday'],
            email=request.POST['email'],
            password=hashed,
        )
        new_user.save()
        request.session['logged_in'] = new_user.id;
        is_valid = True
        return is_valid

    def login(self,request):
        is_valid = True
        user= User.objects.filter(email=request.POST['email']).first()
        if user.email != request.POST['email']:
            messages.error(request, "The user does not exist")
            is_valid = False
            return is_valid
        dbpw=bcrypt.hashpw(request.POST['password'].encode('utf-8'), user.password.encode('utf-8'))
        if dbpw != user.password:
            messages.error(request, "Either email or password is incorrect")
            is_valid = False
            return is_valid
        #when password is correct
        request.session['logged_in'] = user.id
        return is_valid

    def logout(self,request):
        is_valid=True
        del request.session['logged_in']
        return True
class AppManager(models.Manager):
    def createapp(self,request):
        is_valid = True
        if request.POST['date'] == 0:
            messages.error(request,'Please choose current and future date')
            is_valid = False
        if len(request.POST['task']) == 0:
            is_valid = False
            messages.error(request,'Task is required.')
        if len(request.POST['date']) == 0:
            is_valid = False
            messages.error(request,'Date is required.')
        if len(request.POST['time']) == 0:
            is_valid = False
            messages.error(request,'Time is required.')
        if not is_valid:
            return is_valid
        curr_user=User.objects.filter(id=request.session['logged_in']).first()
        new_app=Appointment(
            task=request.POST['task'],
            time=request.POST['time'],
            date=request.POST['date'],
            user=curr_user,
            status='Pending'
        )
        new_app.save()
        is_valid = True
        return is_valid
    def editapp(self,request):
        curr_user=User.objects.filter(id=request.session['logged_in']).first()
        new_date = datetime.strptime(request.POST['date'],'%Y-%m-%d')
        new_time = datetime.strptime(request.POST['time'],'%H:%M')
        print "*"*50
        print new_time
        edit_app=Appointment(
            task=request.POST['task'],
            time=new_time,
            date=new_date,
            user=curr_user,
            status=request.POST['status']
        )
        edit_app.save()
        is_valid = True
        return is_valid

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    bday = models.DateField(auto_now=False, auto_now_add=False)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
class Appointment(models.Model):
    task=models.CharField(max_length=255)
    user=models.ForeignKey(User, related_name ="tasks")
    date = models.DateField(auto_now=False, auto_now_add=False)
    time=models.TimeField(auto_now_add=False,auto_now=False)
    status=models.CharField(max_length=255)

    objects = AppManager()
