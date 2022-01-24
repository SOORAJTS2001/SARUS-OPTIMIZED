from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from numpy import maximum
from .models import CollegeReg, CollegeSignIn,BranchReg
class CollegeRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CollegeReg
        fields=['college_name','password']
class CollegeSignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CollegeSignIn
        fields=['college_name','password']
class BranchRegForm(forms.ModelForm):
    start_year = (
        (2017, 2017), 
        (2018, 2018), 
        (2019, 2019), 
        (2020, 2020), 
        (2021, 2021),
    )
    end_year = (
    (2021, 2021), 
    (2022, 2022), 
    (2023, 2023), 
    (2024, 2024), 
    (2025, 2025),
)
    courses =(
        ("B-TECH","B-TECH"),
        ("M-TECH","M-TECH"),
        ("MCA","MCA"),
    )
    year_start = forms.ChoiceField(choices=start_year)
    year_end = forms.ChoiceField(choices=end_year)
    course = forms.ChoiceField(choices=courses)
    class Meta:
        model = BranchReg
        fields = ['college_name','course','branch_name','division','year_start','year_end']