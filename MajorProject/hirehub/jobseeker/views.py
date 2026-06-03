from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from django.utils import timezone

# Create your views here.
def jobseekerdash(request):
    if "jsid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    context = {
        'js' : js,
        'jsid' : jsid
    }
    return render(request, "jobseeker/jobseekerdash.html",context)

def jslogout(request):
    if "jsid" not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    del request.session['jsid']
    messages.success(request, 'Logged out successfully')
    return redirect('index')

def jsprofile(request):
    if "jsid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.prefetch_related("skills").get(email=jsid)
    educations = Education.objects.filter(jobseeker=js).order_by("-end_year", "-start_year")
    experiences = Experience.objects.filter(jobseeker=js).order_by("-start_date")
    context = {
        'js':js,
        'educations': educations,
        'experiences': experiences,
    }
    return render(request, "jobseeker/jsprofile.html",context)

def jsupdate(request):
    if "jsid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    educations = Education.objects.filter(jobseeker=js)
    experiences = Experience.objects.filter(jobseeker=js)
    context = {
        'js':js,
        'educations': educations,
        'experiences' : experiences,
    }
    if request.method == "POST":
        js.first_name = request.POST.get('first_name')
        js.last_name = request.POST.get('last_name')
        js.dob = request.POST.get('dob')
        js.gender = request.POST.get('gender')
        js.contact_no = request.POST.get('contact_no')
        js.locality = request.POST.get('locality')
        js.city = request.POST.get('city')
        js.district = request.POST.get('district')
        js.zip_code = request.POST.get('zip_code')
        js.state = request.POST.get('state')
        js.country = request.POST.get('country')
        picture = request.FILES.get('picture')
        if picture:
            js.picture = picture
        js.save()
        messages.success(request, "Personal Details saved successfully")
        return redirect('jsupdate')
    return render(request, "jobseeker/jsupdate.html",context)

def appliedjobs(request):
    if "jsid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    applications = JobApplication.objects.filter(jobseeker=js)
    context = {
        'js' : js,
        'jsid' : jsid,
        'applications' : applications
    }
    return render(request, "jobseeker/appliedjobs.html",context)


def save_education(request):
    if "jsid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    if request.method == "POST":
        degree_name = request.POST.get('degree_name')
        specialization = request.POST.get('specialization')
        institute = request.POST.get('institute')
        university = request.POST.get('university')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        Education.objects.create(jobseeker=js,degree_name=degree_name,
                                 specialization=specialization,institute=institute,
                                 university=university,start_year=start_year,
                                 end_year=end_year)
        messages.success(request, "Education added successfully")
        return redirect('jsupdate')
    else:
        messages.error(request, "Something went wrong!")
        return redirect('login')


def save_experience(request):
    if "jsid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        designation = request.POST.get('designation')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        Experience.objects.create(jobseeker=js, company_name=company_name,
                                   designation=designation,start_date=start_date,
                                   end_date=end_date,description=description)
        messages.success(request, "Experience added successfully")
        return redirect('jsupdate')
    else:
        messages.error(request, "Something went wrong!")
        return redirect('login')
        
def save_additional(request):
    if "jsid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    if request.method == "POST":
        resume = request.FILES.get('resume')
        if resume:
            js.resume = resume
        cv = request.FILES.get('cover_letter')
        if cv:
            js.cover_letter = cv
        js.expected_salary  = request.POST.get('expected_salary')
        js.current_salary  = request.POST.get('current_salary')
        js.notice_period  = request.POST.get('notice_period')
        js.linkedin_url  = request.POST.get('linkedin_url')
        js.github_url  = request.POST.get('github_url')
        js.portfolio_url  = request.POST.get('portfolio_url')
        work = request.POST.get('is_open_to_work')
        if work == 'on':
            js.is_open_to_work = True
        else:
            js.is_open_to_work = False
        js.save()
        messages.success(request, "Additional Details saved")
        return redirect('jsupdate')
    else:
        messages.error(request, "Something went wrong!")
        return redirect('login')


def save_skill(request):
    if "jsid" not in request.session:
        messages.error(request, "Login Required")
        return redirect('login')

    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)

    if request.method == "POST":
        skill_names = request.POST.get("skills_input")

        if skill_names:
            skill_list = [s.strip() for s in skill_names.split(",") if s.strip()]
            skill_objects = []

            for name in skill_list:
                skill_obj, created = Skill.objects.get_or_create(
                    skill_name__iexact=name,
                    defaults={"skill_name": name}
                )
                skill_objects.append(skill_obj)
            js.skills.set(skill_objects)
        
        js.save()
        messages.success(request, "Skills Updated Successfully")
        return redirect("jsupdate")

    return redirect('jsupdate')

def apply(request, jobid):
    if "jsid" not in request.session:
        messages.error(request, "You must be logged in before applying any job.")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    job = Job.objects.get(id=jobid)

    if job.is_active == False:
        messages.error(request, "Job is no logner accepting applications")
        return redirect('jobdetails', jobid=job.id)
    if job.deadline < timezone.now().date():
        messages.error(request, "Deadline has been passed")
        return redirect('jobdetails', jobid=job.id)
    
    if JobApplication.objects.filter(jobseeker=js,job=job):
        messages.warning(request, "You have already applied for this job.")
        return redirect('jobdetails', jobid=job.id)

    JobApplication.objects.create(
        jobseeker = js,
        job = job
    )
    messages.success(request, "Applied Successfully, You can also track application status")
    return redirect('jobdetails', jobid=job.id)