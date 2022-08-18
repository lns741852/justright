"""HRCS_RestfulAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from TEST.apis import post  # 從TEST.apis引入post這個函式
from HRCS.apis import getWorkovertimeQuery  # 從TEST.apis引入post這個函式
from HRCS.apis import exportRMPQuery 
from HRCS.apis import Shiftdata
from HRCS.apis import Shiftdata_del
#from HRCS.apis import getAttendancedata
from HRCS.apis import ResetPassword
from HRCS.apis import ForgetPassword
from HRCS.apis import Login
from HRCS.apis import RefreshJWTToken
from HRCS.apis import getAttendanceEmpViewdata
from HRCS.apis import getAttendanceEmpViewQuery
from HRCS.apis import getShiftsAttendanceEmpViewQuery
from HRCS.apis import attendanceData
from HRCS.apis import getEmpdata
from HRCS.apis import getCompanydata
from HRCS.apis import getGroupdata
from HRCS.apis import getDepdata
from HRCS.apis import verifyReset
from HRCS.apis import getTimePeriod
from HRCS.apis import getWorkpositionList
from HRCS.apis import Workovertime_del
from HRCS.apis import Delete_Attend_Punch
from TEST.apis import getRestdata
from TEST.apis import getEmpdata as testEmpdata
from TEST.apis import testShiftdata
import TEST.views as views
urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('test/post/', post),  # 位置寫在這
    #re_path(r'^files/(?P<filename>[^/]+)$' , views.FileUploadView.as_view()), 
    path('HRCS/Shiftdata', Shiftdata),
    re_path(r'^HRCS/Shiftdata/(?P<shiftno>[a-z A-Z 0-9]+)$', Shiftdata_del),
    #re_path(r'^HRCS/Workovertime_del/(?P<overtime_no>[a-z A-Z 0-9]+)$', Workovertime_del),
    #<shiftno>為捕獲的參數使用的變數 [a-z A-Z 0-9]為條件 請參照正則表示式原則
    #path('HRCS/getAttendancedata', getAttendancedata),
    path('HRCS/ForgetPassword',ForgetPassword),
    path('HRCS/ResetPassword', ResetPassword),
    path('test/getRestdata', getRestdata),
    path('test/Shiftdata', testShiftdata),
    path('HRCS/Login', Login),
    path('HRCS/attendanceData', attendanceData),
    path('HRCS/RefreshJWTToken',RefreshJWTToken),
    path('HRCS/getAttendanceEmpViewdata',getAttendanceEmpViewdata),
    path('HRCS/getAttendanceEmpViewQuery',getAttendanceEmpViewQuery),
    path('HRCS/getShiftsAttendanceEmpViewQuery',getShiftsAttendanceEmpViewQuery),
    path('HRCS/getWorkOvertimeQuery',getWorkovertimeQuery),
    path('HRCS/exportRMPQuery',exportRMPQuery),
    path('HRCS/getEmpdata',getEmpdata),
    path('HRCS/getCompanydata',getCompanydata),
    path('HRCS/getGroupdata',getGroupdata),
    path('HRCS/getDepdata',getDepdata),
    path('HRCS/getTimePeriod',getTimePeriod),
    path('TEST/getEmpdata',testEmpdata),
    path('HRCS/verifyReset',verifyReset),
    path('HRCS/getWorkpositionList',getWorkpositionList),
    path('HRCS/deleteAttendPunch',Delete_Attend_Punch)

]

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

