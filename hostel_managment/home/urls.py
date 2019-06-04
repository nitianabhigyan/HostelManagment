from django.urls import path,include
from . import views

"""
Adding verification layers.
Remove hardcoded urls from all pages (use url names instead).
Increase the physical security of database.
Remove all the print() statements [if any].
Implement a local server to send mail.
"""
urlpatterns = [
        path(r'', views.index, name='home_page'),
		path(r'home/' ,views.index, name='home'),
		path(r'reset/', include('password_reset.urls'), name='reset'),
		# find where is this being used and delete it.
		path(r'signup/',views.signup, name='sign_up'),
		path(r'login_attempt',views.password_check,name="password_manage"),
		path('home/student/', include('student.urls'),name = 'student_logged_in'),
        ]
