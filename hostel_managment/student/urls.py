from django.urls import path,include
from . import views
# Create your views here.

urlpatterns = [
        path (r'',views.index, name = 'student_logged_in'),
		path (r'application',views.application, name = 'application'),
		path (r'new_complaint', views.new_complaint, name="new_complaint"),
		path (r'logout', views.logout, name="logout"),
		path(r'alter_student',views.alter_student, name ="alter_student"),
        ]
