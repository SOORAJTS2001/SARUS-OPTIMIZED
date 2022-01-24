from __future__ import division
from django.db import models

# Create your models here.
class CollegeReg(models.Model):
    college_name = models.CharField(max_length=500, unique=True)
    def __str__(self):
        return self.college_name
class CollegeSignIn(models.Model):
    college_name = models.CharField(max_length=500, unique=True)
    def __str__(self):
        return self.college_name
class BranchReg(models.Model):
    college_name = models.CharField(max_length=500,default='',null=False)   
    branch_name = models.CharField(max_length=500,default='',null=False)
    division = models.CharField(max_length=500,default='',null=False)
    def __str__(self):
        return self.college_name,self.branch_name,self.division

    