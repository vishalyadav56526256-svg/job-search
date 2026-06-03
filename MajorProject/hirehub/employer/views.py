from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *

# Create your views here.
def employerdash(request):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    context = {
        'empid':empid,
        'emp' : emp,
    }
    return render(request, "employer/employerdash.html",context)

def emplogout(request):
    if "empid" not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    del request.session['empid']
    messages.success(request, 'Logged out successfully')
    return redirect('index')

def empupdate(request):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    context = {
        'empid':empid,
        'emp' : emp,
    }
    if request.method == "POST":
        emp.first_name = request.POST.get('first_name')
        emp.last_name = request.POST.get('last_name')
        emp.dob = request.POST.get('dob')
        emp.gender = request.POST.get('gender')
        emp.contact_no = request.POST.get('contact_no')
        picture = request.FILES.get('picture')
        if picture:
            emp.picture = picture
        emp.designation = request.POST.get('designation')
        emp.save()
        messages.success(request, "Profile updated successfully")
        return redirect('empupdate')
    return render(request, "employer/empupdate.html",context)

def empprofile(request):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    context = {
        'empid':empid,
        'emp' : emp,
    }
    return render(request, "employer/empprofile.html",context)

def viewjobs(request):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    emp_jobs = Job.objects.filter(employer=emp)
    context = {
        'empid':empid,
        'emp' : emp,
        'emp_jobs' : emp_jobs
    }
    return render(request, "employer/viewjobs.html",context)

def postjob(request):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    all_skills = Skill.objects.all()
    context = {
        'empid':empid,
        'emp' : emp,
        'all_skills' : all_skills,
    }
    if request.method == "POST":
        title = request.POST.get('title')
        job_type = request.POST.get('job_type')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        vacancy = request.POST.get('vacancy')
        deadline = request.POST.get('deadline')
        skills_required = request.POST.get('skills_required')
        description = request.POST.get('description')
        if not emp.company:
            messages.warning(request, "You haven't added company information yet, please add your company details")
            return redirect('postjob')
        job = Job.objects.create(employer=emp,company=emp.company,title=title,
                            job_type=job_type,salary=salary,location=location,
                            vacancy=vacancy,deadline=deadline,description=description)
        if skills_required:
            job_skill = []
            skill_names = [s.strip() for s in skills_required.split(',') if s.strip()]
            for name in skill_names:
                skill, created = Skill.objects.get_or_create(
                    skill_name__iexact = name,defaults={'skill_name':name}
                )
                job_skill.append(skill)
            job.skills_required.set(job_skill)
        job.save()
        messages.success(request, "Job posted successfully")
        return redirect('postjob')
    return render(request, "employer/postjob.html",context)

def add_company(request):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('email')
        logo = request.FILES.get('logo')
        industry = request.POST.get('industry')
        established_at = request.POST.get('established_at')
        website = request.POST.get('website')
        location = request.POST.get('location')
        details = request.POST.get('details')
        if emp.company:
            comp = emp.company
            comp.company_name = company_name
            comp.contact_no = contact_no
            comp.email = email
            comp.industry = industry
            comp.established_at = established_at
            comp.website = website
            comp.location = location
            comp.details = details
            if logo:
                comp.logo = logo
            comp.save()
            messages.success(request, "Company details updated successfully.")
        else:
            comp = Company.objects.create(
                company_name=company_name,
                contact_no=contact_no,
                email=email,
                logo=logo,
                industry=industry,
                established_at=established_at,
                website=website,
                location=location,
                details=details
            )
            emp.company = comp
            emp.save()
            messages.success(request, "Company added successfully.")
        return redirect('empupdate')
    else:
        messages.error(request, "Something went wrong.")
        return redirect('login')

def viewapplicants(request, jobid):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    empid = request.session.get('empid')
    emp = Employer.objects.get(email=empid)
    job = Job.objects.get(id=jobid)
    applications = JobApplication.objects.filter(job=job)
    context = {
        'empid':empid,
        'emp' : emp,
        'job' : job,
        'applications': applications
    }
    return render(request, "employer/viewapplicants.html",context)

def updatestatus(request, appid):
    if "empid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    app = JobApplication.objects.get(id=appid)
    if request.method == "POST":
        status = request.POST.get('status')
        app.status = status
        app.save()
        messages.success(request, "Application status updated successfully")
        return redirect('viewapplicants',jobid=app.job.id)
    else:
        return redirect('viewapplicants',jobid=app.job.id)