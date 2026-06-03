from django.urls import path
from . import views

urlpatterns = [
    path('employerdash/',views.employerdash, name='employerdash'),
    path('emplogout/',views.emplogout, name='emplogout'),
    path('empupdate/',views.empupdate, name='empupdate'),
    path('empprofile/',views.empprofile, name='empprofile'),
    path('viewjobs/',views.viewjobs, name='viewjobs'),
    path('postjob/',views.postjob, name='postjob'),
    path('add_company/',views.add_company, name='add_company'),
    path('viewapplicants/<int:jobid>',views.viewapplicants, name='viewapplicants'),
    path('updatestatus/<int:appid>',views.updatestatus, name='updatestatus'),
]