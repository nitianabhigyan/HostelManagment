from django.urls import path,re_path
from . import views


urlpatterns = [
		path (r'',views.index, name = 'password_reset'),
		path (r'reset_check',views.change, name = 'reset_check'),
		# this regex handles both alphabets and numbers
		re_path(r'(?P<token1>\w+)/', views.token_verification, name='reset_verify'),
        ]
