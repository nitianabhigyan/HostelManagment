"""hostel_managment URL Configuration
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""
from django.contrib import admin
from django.urls import path,include

admin.site.site_header = 'Hostel Managment'
admin.site.site_title = 'Hostel Warden'
admin.site.index_title = 'Hostel administration'
admin.empty_value_display = '**Empty**'
# to be used in finished cases.
#admin.site.site_url = 'http://nitnagaland.ac.in/'
#admin.site.index_template and admin.site.app_template
# to add custom html css templates

urlpatterns = [
    path(r'',include('home.urls'), name='home'),
	path('admin/', admin.site.urls),
	path('entry/',include('entry_exit.urls'),name='entry_exit'),
]
