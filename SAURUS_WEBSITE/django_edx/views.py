from __future__ import division
from pickle import TRUE
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect
from . import firebase
firebase = firebase.FirebaseApplication('https://pi-saurus-default-rtdb.firebaseio.com/', None)
import random
# from django.contrib.auth import authenticate,login
# from django.contrib.auth.forms import UserCreationForm
from .forms import CollegeRegForm, CollegeSignInForm,BranchRegForm
import random
def CollegeRegister(request):
    if request.method == 'POST':
        form = CollegeRegForm(request.POST)
        if form.is_valid():
            # 'college_name','password','unique_id'
            college_name = form.cleaned_data['college_name'].upper()
            password = form.cleaned_data['password']
            fireget = firebase.get('COLLEGE-PASSWORDS','College-Password')
            fireget_dict = eval(fireget)
            if college_name in fireget_dict:
                messages.warning(request, f'{college_name} is already registered with us!!')
            else:
                fireget_dict[college_name] = password
                firebase.put('COLLEGE-PASSWORDS','College-Password',str(fireget_dict))
                admin_code = college_name[:3]+ 'ADM' + str(random.randint(100,100000))
                admin_value = [college_name,'Admin']
                code = {admin_code:admin_value}
                data = {
                    "Student-codes":str(code)
                }
                print(admin_code)
                firebase.patch('SPECIALCODES',data)
                messages.success(request, f'Form submission successful for {college_name} with admin code {admin_code}')
        return render(request,"django_edx/CollegeRegister.html")
    else:
        form = CollegeRegForm()
    return render(request,"django_edx/CollegeRegister.html",{"form":form})
def CollegeSigIn(request):
    if request.method == 'POST':
        form = CollegeSignInForm(request.POST)
        if form.is_valid():
            # 'college_name','password','unique_id'
            college_name = form.cleaned_data['college_name']
            password = form.cleaned_data['password']
            fireget = firebase.get('COLLEGE-PASSWORDS','College-Password')
            fireget_dict = eval(fireget)
            if college_name in fireget_dict:
                messages.success(request, f'{college_name} has been signed in')
               
            else:
                messages.warning(request, f"Seems that your college {college_name} haven't registered")
        return render(request,"django_edx/CollegeSignIn.html",{"Sign_In":True})
    else:
        form = CollegeSignInForm()
        messages.warning(request, f'Please try to resubmit the form!!')
    return render(request,"django_edx/CollegeSignIn.html",{"form":form})
def BranchRegView(request):
    if request.method == 'POST':
        form = BranchRegForm(request.POST)
        if form.is_valid():
            # 'college_name','password','unique_id'
            college_name = form.cleaned_data['college_name'].upper()
            branch_name = form.cleaned_data['branch_name'].upper()
            start = form.cleaned_data['year_start']
            end = form.cleaned_data['year_end']
            course = str(form.cleaned_data['course'])
            batch = str(start) +'-'+str(end)
            batch_name =  str(start[2:5]) +'-'+str(end[2:5])
            print(course)
            division_name = form.cleaned_data['division'].upper()
            fireget = firebase.get('SPECIALCODES','Student-codes')
            fire_college_get = firebase.get('COLLEGE-PASSWORDS','College-Password')
            fireget_college_dict = eval(fire_college_get)
            fireget_dict = eval(fireget)
            check = False
            if college_name in fireget_college_dict:
                for i in list(fireget_dict.values()):
                    if college_name in i[0] and course in i[1]  and branch_name in i[2] and batch in i[3] and division_name in i[4]:
                        check = True
                print(check)
                if check  == True:
                    messages.warning(request,f"Hey! {college_name} {branch_name} {batch} is already there..")
                    print(check)
                else:
                    empty_stu =[]
                    empty_tea =[]
                    empty_rep =[]
                    empty_stu.append(college_name)
                    empty_stu.append(course)
                    empty_stu.append(branch_name)
                    empty_stu.append(batch)
                    empty_stu.append(division_name)
                    empty_stu.append('Student')
                    empty_rep.append(college_name)
                    empty_rep.append(course)
                    empty_rep.append(branch_name)
                    empty_rep.append(batch)
                    empty_rep.append(division_name)
                    empty_rep.append('Representative')
                    empty_tea.append(college_name)
                    empty_tea.append(course)
                    empty_tea.append(branch_name)
                    empty_tea.append(batch)
                    empty_tea.append(division_name)
                    empty_tea.append('Teacher')
                    student_key =college_name[:3] + 'STU'+ str(batch_name) + branch_name + str(random.randint(100,10000))
                    rep_key = college_name[:3] +'REP'+ str(batch_name) + branch_name + str(random.randint(100,10000))
                    teacher_key = college_name[:3] +'TEAC'+ str(batch_name) + branch_name + str(random.randint(100,10000))
                    fireget_dict[student_key] = empty_stu
                    fireget_dict[rep_key] = empty_rep
                    fireget_dict[teacher_key] = empty_tea
                    print(fireget_dict)
                    data = {
                        'Sessions':"{}"
                    }
                    firebase.patch(f'STORED-DATA/{college_name}',data)
                    data = {
                        'stored-data':"{}"
                    }
                    firebase.patch(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}',data)
                    data = {
                            'code-abbreviations':'{}'
                        }
                    firebase.patch(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}',data)
                    data = {
                            'meta-data':"{'links':0,'photo_size':0,'doc_size':0,'photo_no':0,'doc_no':0,'nsfw_alerts':0,'customers':0,'buzzword':''}"
                        }
                    firebase.patch(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}',data)
                    data = {
                        'Students-in-class':"{}"
                    }
                    firebase.patch(f'STORED-DATA/{college_name}/{course}/{branch_name}/{batch}/{division_name}',data)
                    firebase.put('/SPECIALCODES','Student-codes',str(fireget_dict))
                    messages.success(request,f'''Your {course} with {branch_name} branch  and {batch}th batch has been registered on {college_name}
                    \n Please Note the codes for Students : {student_key} StudentRepresentative : {rep_key} Teacher : {teacher_key}''')
            else:
                messages.warning(request,f'''Your {college_name} has not been registered''')

        
        return render(request,"django_edx/BranchReg.html")
    else:
        form = BranchRegForm()
        messages.warning(request, f'Please try to resubmit the form!!')
    return render(request,"django_edx/BranchReg.html",{"form":form})
