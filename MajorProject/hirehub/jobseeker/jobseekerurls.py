from django.urls import path
from . import views

urlpatterns = [
    path('jobseekerdash/',views.jobseekerdash, name='jobseekerdash'),
    path('jslogout/',views.jslogout, name='jslogout'),
    path('jsprofile/',views.jsprofile, name='jsprofile'),
    path('jsupdate/',views.jsupdate, name='jsupdate'),
    path('appliedjobs/',views.appliedjobs, name='appliedjobs'),
    path('save_education/',views.save_education, name='save_education'),
    path('save_experience/',views.save_experience, name='save_experience'),
    path('save_additional/',views.save_additional, name='save_additional'),
    path('save_skill/',views.save_skill, name='save_skill'),
    path('apply/<int:jobid>',views.apply, name='apply'),
]