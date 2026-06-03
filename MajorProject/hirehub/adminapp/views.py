from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
# Create your views here.

def admindash(request):
    if "adminid" not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    adminid = request.session.get('adminid')
    context = {
        'adminid' : adminid
    }
    return render(request, "admin/admindash.html",context)

def viewenq(request):
    if "adminid" not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    adminid = request.session.get('adminid')
    enqs = Enquiry.objects.all()
    context = {
        'adminid' : adminid,
        'enqs' : enqs
    }
    return render(request, "admin/viewenq.html",context)

def adminlogout(request):
    if "adminid" not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    del request.session['adminid']
    messages.success(request, 'Logged out successfully')
    return redirect('index')

def changepassword(request):
    if "adminid" not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    adminid = request.session.get('adminid')
    context = {
        'adminid' : adminid
    }
    if request.method == "POST":
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        admin = LoginInfo.objects.get(username = adminid)
        if newpwd != confirmpwd:
            messages.warning(request, "New password & confirm password not matched.")
            return redirect('changepassword')
        elif admin.password != oldpwd:
            messages.error(request, "Old password didn't matched !!")
            return redirect('changepassword')
        elif admin.password == newpwd:
            messages.warning(request, "Password cannot be same as previous passwords.")
            return redirect('changepassword')
        else:
            admin.password = newpwd
            admin.save()
            messages.success(request, "Password Changed successfully")
            return redirect('admindash')
    return render(request, "admin/changepassword.html",context)
