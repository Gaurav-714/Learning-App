from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import stripe

def home(request):
    courses = Course.objects.all()
    context = {'courses' : courses}
    return render(request, 'home.html', context)


def view_course(request, slug):
    course = Course.objects.filter(slug = slug).first()
    course_module = CourseModule.objects.filter(course = course)
    context = {'course' : course, 'course_module' : course_module}
    return render(request, 'course.html', context)


def become_pro(request):
    if request.method == 'POST':
        
        membership = request.POST.get('membership', 'MONTHLY')
        amount = 699
        if membership == 'Quarterly':
            amount = 1999
        elif membership == 'Half_Yearly':
            amount = 3939
        elif membership == 'Yearly':
            amount = 7799
        
        stripe.api_key = "sk_test_51ObestSAg4PJlxn2ze98o4f8NOFeLmCsIruBpoARHOKsXP5eqo0nuSuQlBpY0CkEPurvZHWq86yNwlGrQHQFwV9E00ZDixmqTP"
        customer = stripe.Customer.create(
            email = request.user.email,
        )
        charge = stripe.Charge.create(
            customer = customer,
            amount = amount,
            currency = 'INR',
            description = 'membership'
        )
        
    return render(request, 'become_pro.html')


def login_page(request):
    if request.method == 'POST':

        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.filter(username = username)
            if not user:
                messages.warning(request, "Username Not Found.")
                return redirect('/login/')
            
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                messages.warning(request, "Incorrect Password")
            return redirect('/login/')
        except:
            messages.warning(request, "Somthing went wrong...")
            return redirect('/register/')
        
    return render(request, 'login.html')
        

def register_page(request):
    if request.method == 'POST':

        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.filter(username = username)
            if user.exists():
                messages.warning(request, "Username is already taken.")
                print(messages)
                return redirect('/register/')
            
            user = User.objects.create(username = username)
            user.set_password(password)
            user.save()

            messages.success(request, "Account Created")
            print(messages)
            return redirect('/login/')

        except:
            messages.warning(request, "Something went wrong...")
            print(messages)
            return redirect('/login/')

    return render(request, 'register.html')