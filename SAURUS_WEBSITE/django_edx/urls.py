from django.urls import path
from . import views
urlpatterns = [
    path('Register/',views.CollegeRegister,name = 'Register'),
    path('SignIn/',views.CollegeSigIn,name='SignIn'),
    path('BranchReg/',views.BranchRegView,name='BranchRegister')
]
 


    # path('',views.index,name='home'),
    # path('<a>',views.StudentsView,name='StudentsView')


