from django.conf.urls import url
from django.urls import path
from . import views 

urlpatterns = [
    url(r'^$' , views.Index , name='index'),
    url(r'^login/$' , views.Home , name='home'),
    url(r'^logout/$' , views.Logout , name='logout'),
    url(r'^admin_system/$' , views.Admin_System , name='admin_system'),
    url(r'^view_content/(?P<type_>[-\w\d]+)/$' , views.View_Content, name='view_content'),
    url(r'^add_content/(?P<type_>[-\w\d]+)/$' , views.Add_Content, name='add_content'),
    url(r'^view_certificates/$' , views.View_Certificates , name='view_certificates'),
    url(r'^certificate_details/(?P<id>[-\w\d]+)$' , views.Certificate_Details , name='certificate_details'),
    url(r'^add_certificate/$' , views.Add_Certificate, name='add_certificate'),
    url(r'^delete_certificate/(?P<id>\d+)$' , views.Delete_Certificate, name='delete_certificate'),
    url(r'^delete_content/(?P<id>\d+)/(?P<type_>[-\w\d]+)/$' , views.Delete_Content, name='delete_content'),
    url(r'^get_student_data/$' , views.Get_Student_Data ,name='get_student_data'),
    url(r'^mail_qrcodes/$' , views.Mail_QRcodes , name='mail_qrcodes'),
    url(r'^error_page/$' , views.Error_Page , name='error_page'),
    url(r'^select_certificates/$' , views.Select_Certificates , name='select_certificates'),
    url(r'^edit_student/(?P<id>\d+)/$' , views.Edit_Student, name='edit_student'),
    url(r'^redirect_to_url/$' , views.Redirect_To_Url , name='redirect_to_url'),
    url(r'^get_request/$' , views.Get_Request , name='get_request'),
    url(r'^requests/$' , views.Show_Requests , name='requests'),
    url(r'^accept_request/(?P<id>\d+)/$' , views.Accept_Request , name='accept_request'),
    url(r'^delete_request/(?P<id>\d+)/$' , views.Delete_Request , name='delete_request'),

]
