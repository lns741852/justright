from django.db import models
import django_filters
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Token(models.Model):
    emp_no = models.CharField(db_column='EMP_NO', max_length=20,primary_key=True)  # Field name made lowercase.
    token = models.CharField(max_length=500)
    deadline = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'TOKEN'

class ZzEmpTable(models.Model):  # 基本上就是python manage.py inspectdb指令出來的複製貼上
   # emp_id = models.AutoField(db_column='EMP_ID')  # Field name made lowercase.
    # Field name made lowercase.
    emp_no = models.CharField(
        db_column='EMP_NO', primary_key=True, max_length=50)
    # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', max_length=30)
    # Field name made lowercase.
    dep_no = models.CharField(db_column='DEP_NO', max_length=20)
    # Field name made lowercase.
    user_no = models.CharField(db_column='USER_NO', max_length=20)
    # Field name made lowercase.
    user_pwd = models.CharField(db_column='USER_PWD', max_length=20)
    line_id = models.CharField(max_length=50)
    tel = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zz_EMP_TABLE'
        unique_together = (('emp_no', 'line_id'),)

    def __str__(self):  # 其實不確定這行的用處 但姑且加上去免得出甚麼錯 如果有問題就隔離
        return str(self.author) + ":" + str(self.content)


class CompanyTable(models.Model):
    comp_id = models.CharField(db_column='COMP_ID', max_length=11)
    comp_no = models.CharField(
        db_column='COMP_NO', primary_key=True, max_length=20)
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)
    comp_name = models.CharField(db_column='COMP_NAME', max_length=50)

    class Meta:
        managed = False
        db_table = 'COMPANY_TABLE'


class RestTable(models.Model):
    rest_id = models.CharField(db_column='REST_ID', max_length=11)
    rest_no = models.CharField(
        db_column='REST_NO', primary_key=True, max_length=20)
    attend_no = models.CharField(db_column='ATTEND_NO', max_length=20)
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)
    rest_type = models.IntegerField(db_column='REST_TYPE')
    app_date = models.DateField(db_column='APP_DATE')
    rest_date = models.DateField(db_column='REST_DATE')
    rest_reason = models.TextField(db_column='REST_REASON')

    class Meta:
        managed = False
        db_table = 'REST_TABLE'


class RestType(models.Model):
    rest_type_id = models.CharField(db_column='REST_TYPE_ID', max_length=11)
    rest_type_no = models.IntegerField(
        db_column='REST_TYPE_NO', primary_key=True)
    rest_no = models.CharField(db_column='REST_NO', max_length=20)
    type_name = models.CharField(db_column='TYPE_NAME', max_length=20)

    class Meta:
        managed = False
        db_table = 'REST_TYPE'


class AttendanceTable(models.Model):
    attend_id = models.CharField(db_column='ATTEND_ID', max_length=11)  # Field name made lowercase.
    attend_date = models.DateField(db_column='ATTEND_DATE')  # Field name made lowercase.
    attend_no = models.CharField(db_column='ATTEND_NO', primary_key=True, max_length=20)  # Field name made lowercase.
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', max_length=20)  
# Field name made lowercase.
    shift_no = models.CharField(db_column='SHIFT_NO', max_length=20)  
# Field name made lowercase.
    punch_in = models.DateTimeField(db_column='PUNCH_IN', blank=True, 
null=True)  # Field name made lowercase.
    punch_out = models.DateTimeField(db_column='PUNCH_OUT', blank=True, null=True)  # Field name made lowercase.
    in_position = models.CharField(db_column='IN_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    out_position = models.CharField(db_column='OUT_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    overtime_no = models.CharField(db_column='OVERTIME_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    comp_no = models.CharField(db_column='COMP_NO', max_length=20)  # Field name made lowercase.
    salary_no = models.CharField(db_column='SALARY_NO', max_length=20)  # Field name made lowercase.
    total_time = models.IntegerField(blank=True, null=True)
    fulltime = models.IntegerField(blank=True, null=True)
    latetime = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ATTENDANCE_TABLE'

class ShiftsTable(models.Model):
    # shift_id = models.CharField(db_column='SHIFT_ID', max_length=11)  # 排班表流水號
    shift_no = models.CharField(
        db_column='SHIFT_NO', primary_key=True, max_length=20)  # 排班表編號
    attend_no = models.CharField(
        db_column='ATTEND_NO', max_length=20, blank=True, null=True)  # 出勤表編號
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)  # 員工編號
    date = models.DateField(db_column='DATE')  # 日期
    punch_in = models.DateTimeField(
        db_column='PUNCH_IN', blank=True, null=True, auto_now=True)  # 出勤時間 auto_now=True避免空值錯誤
    punch_out = models.DateTimeField(
        db_column='PUNCH_OUT', blank=True, null=True, auto_now=True)  # 下班時間 auto_now=True避免空值錯誤
    text = models.TextField(db_column='TEXT')  # 文字備註

    class Meta:
        managed = False
        db_table = 'SHIFTS_TABLE'


class RestTable(models.Model):
    # Field name made lowercase.
    rest_id = models.CharField(db_column='REST_ID', max_length=11)
    # Field name made lowercase.
    rest_no = models.CharField(
        db_column='REST_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    attend_no = models.CharField(db_column='ATTEND_NO', max_length=20)
    # Field name made lowercase.
    rest_type = models.IntegerField(db_column='REST_TYPE')
    # Field name made lowercase.
    app_date = models.DateField(db_column='APP_DATE')
    # Field name made lowercase.
    rest_date = models.DateField(db_column='REST_DATE')
    # Field name made lowercase.
    rest_reason = models.TextField(db_column='REST_REASON')

    class Meta:
        managed = False
        db_table = 'REST_TABLE'

class EmpTable(models.Model):
    emp_id = models.CharField(db_column='EMP_ID', max_length=11)  # Field name made lowercase.
    emp_no = models.CharField(db_column='EMP_NO', primary_key=True, max_length=20)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', unique=True, max_length=20)  # Field name made lowercase.
    comp_no = models.CharField(db_column='COMP_NO', max_length=20)  # Field name made lowercase.
    dep_no = models.CharField(db_column='DEP_NO', max_length=20)  # Field name made lowercase.
    work_position = models.CharField(db_column='WORK_POSITION', max_length=20)  # Field name made lowercase.
    user_pwd = models.CharField(db_column='USER_PWD', max_length=500)  # Field name made lowercase.
    line_id = models.CharField(max_length=50)
    tel = models.CharField(max_length=10, blank=True, null=True)
    group_no = models.CharField(db_column='GROUP_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    group_leader = models.IntegerField(db_column='GROUP_leader', blank=True, null=True)  # Field name made lowercase.
    working = models.IntegerField(db_column='WORKING', blank=True, null=True)  # Field name made lowercase.
    auth = models.CharField(db_column='AUTH', max_length=1)  # Field name made lowercase.
    mail = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'EMP_TABLE'
        unique_together = (('emp_no', 'line_id'),)


class JwtToken(models.Model):
    username = models.CharField(primary_key=True,max_length=45)
    token = models.CharField(max_length=400)
    exp_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'JWT_TOKEN'

class AttendanceEmpView(models.Model):
    attend_date = models.DateField(db_column='ATTEND_DATE')  # Field name made lowercase.
    attend_no = models.CharField(db_column='ATTEND_NO', primary_key=True, max_length=20)  # Field name made lowercase.
    shift_no = models.CharField(db_column='SHIFT_NO', max_length=20)  
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', max_length=20)  # Field name made lowercase.
    group_no = models.CharField(db_column='GROUP_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    punch_in = models.DateTimeField(db_column='PUNCH_IN', blank=True, null=True)  # Field name made lowercase.
    punch_out = models.DateTimeField(db_column='PUNCH_OUT', blank=True, null=True)  # Field name made lowercase.
    in_position = models.CharField(db_column='IN_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    out_position = models.CharField(db_column='OUT_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    overtime_no = models.CharField(db_column='OVERTIME_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    salary_no = models.CharField(db_column='SALARY_NO', max_length=20)  # Field name made lowercase.
    total_time = models.IntegerField(blank=True, null=True)
    fulltime = models.IntegerField(blank=True, null=True)
    latetime = models.IntegerField(blank=True, null=True)
    attend_id = models.CharField(db_column='ATTEND_ID', max_length=11)  # Field name made lowercase.
    comp_name = models.CharField(db_column='COMP_NAME', max_length=50)
    tel = models.CharField(max_length=10, blank=True, null=True)
    work_position = models.CharField(db_column='WORK_POSITION', max_length=20)  # Field name made lowercase.   

    class Meta:
        managed = False
        db_table = 'attendance_emp_view'


class WorkOvertime(models.Model):
    overtime_id = models.CharField(db_column='OVERTIME_ID', max_length=20)  # Field name made lowercase.
    overtime_no = models.CharField(db_column='OVERTIME_NO', primary_key=True, max_length=20)  # Field name made lowercase.
    attend_no = models.CharField(db_column='ATTEND_NO', max_length=20)  # Field name made lowercase.
    overtime_pay_no = models.CharField(db_column='OVERTIME_PAY_NO', max_length=20)  # Field name made lowercase.
    overtime_date = models.DateField(db_column='OVERTIME_DATE')  # Field name made lowercase.
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)  # Field name made lowercase.
    punch_in = models.DateTimeField(db_column='PUNCH_IN', blank=True, null=True)  # Field name made lowercase.
    punch_out = models.DateTimeField(db_column='PUNCH_OUT', blank=True, null=True)  # Field name made lowercase.
    overtime_hours = models.IntegerField(db_column='OVERTIME_HOURS')  # Field name made lowercase.
    overtime_check = models.IntegerField(db_column='OVERTIME_CHECK')  # Field name made lowercase.
    overtime_type_no = models.IntegerField(db_column='OVERTIME_TYPE_NO', blank=True, null=True)  # Field name made lowercase.
    hours_change = models.IntegerField(db_column='HOURS_CHANGE', blank=True, null=True)  # Field name made lowercase.
    disaster = models.IntegerField(db_column='DISASTER', blank=True, null=True)  # Field name made lowercase.
    no_rest = models.IntegerField(db_column='NO_REST', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WORK_OVERTIME'
        unique_together = (('overtime_no', 'overtime_id'),)