import qrcode 
import io
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid 




from django.db import models

# Create your models here.

Gender_Choices=[
    ('M', 'male'),
    ('F' ,'female'),
    ('O' ,'other')
]
class Courses(models.Model):
    Course_name  = models.CharField(max_length = 50 , null=True)
    def __str__(self):
        return str(self.Course_name)

class Students(models.Model):
    Name = models.CharField(max_length = 30 , null= True)
    Guardian_Name = models.CharField(max_length = 30 , null=True)
    Email = models.EmailField()
    Address = models.TextField(null=True)
    DOB = models.DateField(null=True)
    Gender = models.CharField(max_length=5 , choices = Gender_Choices , null=True)
    Age = models.IntegerField(null=True)
    High_School = models.CharField(max_length=50  , null=True)



    def __str__(self):
        return str(self.Name)

    def get_abs_url(self):
        return reverse("edit_student", kwargs={"id":self.id})




class Batches(models.Model):
    Batch_name = models.CharField(max_length=50 , null=True)
    def __str__(self):
        return str(self.Batch_name)


class Certificates(models.Model):
    new_id =models.UUIDField(primary_key = False, default = uuid.uuid4, editable = False , null=True) 
    Student = models.ForeignKey(Students  , on_delete=models.CASCADE  , null=True)
    Course = models.ForeignKey(Courses , on_delete=models.CASCADE  , null=True )
    Batch= models.ForeignKey(Batches , on_delete=models.CASCADE  , null=True )
    Certificate = models.ImageField(upload_to='certificates' , max_length=100 , null=True)
    QRcode = models.ImageField(upload_to='qrcodes',  max_length=100 , null=True , blank=True)
    def __str__(self):
        return str(self.Student)  
    def get_absolute_url(self):
        return reverse('homepage')

    def generate_qrcode(self , request):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        
        url = 'http://'+ request.get_host()  + '/certificate_details/' +  str(self.new_id)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image()

        buffer = io.BytesIO()
        img.save(buffer)
        filename = 'events-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.getvalue, None)
        self.QRcode.save(filename, filebuffer)
   
   
class Requests(models.Model):
    Email = models.EmailField()
    Proof = models.ImageField(upload_to='requests' , max_length=100 , null=True)




