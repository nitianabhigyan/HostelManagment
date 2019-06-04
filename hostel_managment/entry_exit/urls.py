from django.urls import path
from . import views

urlpatterns = [
	 path(r'', views.login,name='login_page'),
	 path(r'guard', views.index, name='guard_home_page'),
	 path(r'guard/logout', views.logout, name='guard_logout'),
	 path(r'check', views.ajax_handler, name='ajaxrespond'),
]
