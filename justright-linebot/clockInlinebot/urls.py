from django.urls import path
from . import views

#URI配置
app_name = 'clockInlinebot'
urlpatterns = [
    path('callback', views.callback),
    path('get_location', views.get_location),
    path('overtime_check', views.overtime_check),
    path('change_shift_time', views.change_shift_time,
	name='change_shift_time'),
    path('overtime_check_save', views.overtime_check_save,
         name='overtime_check_save'),
    path('change_shift_time_save', views.change_shift_time_save,
         name='change_shift_time_save'),
]
