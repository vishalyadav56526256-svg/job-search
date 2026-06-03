from django.urls import path
from . import views
urlpatterns = [
    path('admindash/',views.admindash,name='admindash'),
    path('viewenq/',views.viewenq,name='viewenq'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
]