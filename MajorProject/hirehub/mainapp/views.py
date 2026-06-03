from django.shortcuts import render,redirect
from .forms import EnquiryForm
from django.contrib import messages
from .models import *
from django.db import transaction

# Create your views here.
def index(request):
    newly_added = Job.objects.all().order_by('-created_at')[:5]
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        'newly_added' : newly_added,
        'user': user
    }
    return render(request, "mainapp/index.html",context)

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = LoginInfo.objects.get(username=username, password=password)
            if user and user.usertype == "admin":
                messages.success(request, "Welcome Admin")
                request.session['adminid'] = user.username
                request.session.set_expiry(0)
                return redirect('admindash')
            elif user and user.usertype == "jobseeker":
                messages.success(request, "Welcome Jobseeker")
                request.session['jsid'] = user.username
                request.session.set_expiry(0)
                return redirect('index')
            elif user and user.usertype == "employer":
                messages.success(request, "Welcome Employer")
                request.session['empid'] = user.username
                request.session.set_expiry(0)
                return redirect('index')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid Username or password")
            return redirect('login')
    
    return render(request, "mainapp/login.html")

def register(request):
    if request.method == "POST":
        usertype = request.POST.get('usertype')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        pwd = request.POST.get('pwd')
        confirm_pwd = request.POST.get('confirm_pwd')
        if pwd != confirm_pwd:
            messages.warning(request, "Enter same password")
            return redirect('register')
        exists = LoginInfo.objects.filter(username=email)
        if exists:
            messages.error(request, "This email is already registered.")
            return redirect('register')
        try:
            with transaction.atomic():
                log = LoginInfo(usertype=usertype, username=email, password=pwd)
                if usertype == "jobseeker":
                    js = Jobseeker(user=log,first_name=first_name,last_name=last_name, email=email,contact_no=contact_no)
                    log.save()
                    js.save()
                elif usertype == "employer":
                    emp = Employer(user=log,first_name=first_name,last_name=last_name, email=email,contact_no=contact_no)
                    log.save()
                    emp.save()
                messages.success(request,'Registered successfully. Now login to update profile.')
                return redirect('register')
        except Exception as e:
            messages.error(request, f"Something went wrong {e}")
            return redirect('register')
    
    return render(request, "mainapp/register.html")

def contact(request):
    if request.method == "POST":
        data = EnquiryForm(request.POST)
        if data.is_valid():
            data.save()
            messages.success(request, "Enquiry submitted successfully")
        else:
            messages.error(request, "Failed to sent enquiry, Invalid form data!")
            form = EnquiryForm()
        return redirect('contact')
    else:
        form = EnquiryForm()
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        "form":form,
        'user': user
    }
    return render(request, "mainapp/contact.html", context)

def about(request):
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        'user': user
    }
    return render(request, "mainapp/about.html",context)


def jobdetails(request, jobid):
    job = Job.objects.get(id=jobid)
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        'job':job,
        'user': user
    }
    return render(request, "mainapp/jobdetails.html",context)