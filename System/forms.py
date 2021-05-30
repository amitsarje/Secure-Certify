from django import forms
from .models import *



class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields= [
             'Course_name'
        ]


class AddBatchForm(forms.ModelForm):
    class Meta:
        model = Batches
        fields=[
            'Batch_name'
        ]


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificates
        fields= [
             'Student' , 'Course' , 'Batch' , 'Certificate'
        ]

class CSVForm(forms.Form):
    file = forms.FileField(label="")

class StudentForm(forms.ModelForm):
    DOB = forms.DateField(label='DOB', widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    class Meta:
        model = Students
        fields =[
            'Name','Guardian_Name','Email','Address','DOB','Gender','Age','High_School'
        ]

class RequestForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields =[
            'Email' , 'Proof'
        ]

