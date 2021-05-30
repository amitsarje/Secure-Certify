from django.shortcuts import render , redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from  django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.urls import reverse
from .forms import *
import csv
import datetime
from django.core import mail
from django.core.mail import send_mail , EmailMessage , send_mass_mail
from django.http import HttpResponse



# Create your views here.



#This Function redirect to the public page accessible to all
def Index(request):
    form = RequestForm(None)
    context = {
        'form':form
    }
    return render(request , 'index.html'  , context)



#This function completes login functionality and redirects to admin page after logging in !
def Home(request):
    
        if request.user.is_authenticated:
            return redirect('/admin_system/') #redirecting to the admin page
        else: 
            if request.method == 'POST':
                form = AuthenticationForm(request=request, data=request.POST)
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request , user)
                        return redirect('/admin_system/')
                    else:
                        messages.error(request , "Invalid credentials , Enter again")
                        return redirect('/login/')
                else:
                    messages.error(request , "Invalid credentials , Enter again")
                    return redirect(request.path_info)
            else:
                form =AuthenticationForm() 
                return render(request , 'login.html' ,{'form':form})
    

#This function is used to render admin page (admin-page=homepage.html)
@login_required(login_url='/login/')
def Admin_System(request):
    count = Requests.objects.all().count()
    context ={
        'rcount':count
    }
    return render(request , 'homepage.html' , context)


#logs out a admin
@login_required(login_url='/login/')
def Logout(request):
    logout(request)
    return redirect('/')



#This function gets the certificate details after entering certificate url
def Certificate_Details(request , id):
    try:
        C = Certificates.objects.get(new_id=id)
        context={
            'c':C
        }
        return render(request , 'certificate_details.html' , context)
    except:
        return redirect('/error_page/')


#Handles viewing of Courses/Batches
@login_required(login_url='/login/')
def View_Content(request , type_):
    if type_=="course":
        content = Courses.objects.all()
        form = AddCourseForm(None)
    elif type_=="batch":
        content = Batches.objects.all()
        form  = AddBatchForm(None)
    else:
        return redirect('/admin_system/')
    count = content.count()
    
    context ={
        'content':content, 
        'form':form ,
        'count':count,
        'type':type_
    }
    return render(request , 'view_contents.html' , context)


#handles the adding of courses/batches
@login_required(login_url='/login/')
def Add_Content(request , type_):
    if type_=="course":
        form = AddCourseForm(request.POST)
    else:
        form = AddBatchForm(request.POST)
    if form.is_valid:
        instance = form.save()
        instance.save()
        return redirect(reverse('view_content' , kwargs={'type_':type_} ))


#handles deletion of courses/batches
@login_required(login_url='/login/')
def Delete_Content(request , id , type_):
    if type_=="course":
        Courses.objects.get(id=id).delete()
    else:
        Batches.objects.get(id=id).delete()
    return redirect(reverse('view_content' , kwargs={'type_':type_} ))


#deletion of certificate with given id
@login_required(login_url='/login/')
def Delete_Certificate(request , id):
    Certificates.objects.get(id=id).delete()
    return redirect('/view_certificates/')


#Adding of certificates from admin site is handled via this function/view
@login_required(login_url='/login/')
def Add_Certificate(request):
    form = CertificateForm(request.POST , request.FILES)
    if form.is_valid():
        instance = form.save()
        instance.generate_qrcode(request)
        instance.save()

    return redirect('/view_certificates/')


#Getting certificates and rendering them on to view_certificates.html
@login_required(login_url='/login/')
def View_Certificates(request):
    form = CertificateForm(None)
    C = Certificates.objects.all()
    count = C.count()
    context = {
        'C':C ,
        'form':form,
        'count':count
    }
    return render(request , 'view_certificates.html' , context)




#This function gets csv file from POST Request  , processes it and saves student data in the backend
@login_required(login_url='/login/')
def Get_Student_Data(request):
    if request.method=="POST":
        form  = CSVForm(request.POST , request.FILES)
        if form.is_valid():
            csvfile = form.cleaned_data['file']
            file = csvfile.read().decode("utf-8")	
            lines = file.split("\n")
            counter = 0
            for line in lines:
                if counter==0:
                    counter=1
                    continue
                data = line.split(",")
                try:
                    date = str(data[4])
                    date= datetime.datetime.strptime(date , '%m/%d/%Y')
                    Students.objects.create(Name = data[0] , Guardian_Name =data[1] ,
                    Email=data[2],Address=data[3],DOB=date,Gender=data[5],Age=int(data[6]),High_School=data[7])
                except:
                    break
            messages.success(request , 'Students Added Successfully')
            
        else:
            print("error")
        return redirect('/get_student_data/')
    else:
        S = Students.objects.all()
        form = CSVForm(None)
        context = {
            'form':form ,
            'students':S
        }
        return render(request , 'add_students.html' , context)

#for selecting certificates
@login_required(login_url='/login/')
def Select_Certificates(request):
    C = Certificates.objects.all()
    context ={
        'certificates':C
    }
    return render(request , 'select_certificates.html' , context)



#This function takes Certificates queryset as a parameter and sends qr codes to the mail assigned to it!
def Send_Mails(C):
    try:
        email_list=[]
        for c in list(C):
            email = EmailMessage(
                                '{} - Certificate - {}'.format(c.Student, c.Course),
                                'Body',
                                'abc@gmail.com',
                                [c.Student.Email],
                            )
            email.attach('QR_code-{}.jpg'.format(c.Course) , c.QRcode.read(), 'image/png')
            email_list.append(email)
            print(c)
        connection = mail.get_connection() 
        connection.send_messages(email_list)
    except:
        return redirect('/error_page/')


#Gets the list of certificates from POST requests and calls Send_Mails function
@login_required(login_url='/login/')
def Mail_QRcodes(request):
        List = request.POST.getlist('selected_certificates')
        email_list=[]
        C = []
        print(List)
        for i in List:
            c = Certificates.objects.get(id=i)
            C.append(c)
        Send_Mails(C) #calling Send_Mails function to send the emails
        messages.success(request ,'Certificate QR codes have been sent !')
        return redirect('/select_certificates/')


#Edition of student details handeled via this function
@login_required(login_url='/login/')
def Edit_Student(request , id):
    instance=Students.objects.get(id=id)
    form = StudentForm(request.POST or None , instance=instance)
    if request.method=="POST":
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()
            messages.success(request ,'Student updated successfully' )
        return redirect('/get_student_data/')
    else:
        form = StudentForm(instance = instance)
        context={
            'form':form,
            'id':instance.id
        }
        
    return render(request , 'edit_student.html' ,context)


#Redirecting to the certificate url
def Redirect_To_Url(request):
    url= request.POST.get('Url')
    print(url)
    return redirect(url)


#Getting the request to resend the certificate qr codes
def Get_Request(request):
    form = RequestForm(request.POST , request.FILES)
    if form.is_valid():
        if Students.objects.filter(Email=form['Email'].value()).exists():
            instance = form.save()
            instance.save()
            messages.add_message(request , messages.SUCCESS  ,  'your request has been submitted' , extra_tags='success')
        else:
            messages.add_message(request , messages.ERROR  ,  'No certificate registered with submitted email' , extra_tags='error')

    return redirect('/')

#Showing requests
@login_required(login_url='/login/')
def Show_Requests(request):
    R = Requests.objects.all()
    context ={
        'requests':R
    }
    return render(request , 'requests.html' , context)


#accepting requests and resending mails
@login_required(login_url='/login/')
def Accept_Request(request , id ):
    R = Requests.objects.get(id=id)
    C = Certificates.objects.filter(Student__Email=R.Email)
    Send_Mails(C)
    Requests.objects.get(id=id).delete()
    messages.success(request ,'Certificate QR codes have been sent !')
    return redirect('/requests/')


#deleting requests
@login_required(login_url='/login/')
def Delete_Request(request , id):
    Requests.objects.get(id = id).delete()
    return redirect('/requests/')


#any certificate error occurs , error.html renders
def Error_Page(request):
    return render(request , 'error.html')