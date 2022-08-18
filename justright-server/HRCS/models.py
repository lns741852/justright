from tokenize import group
from django.db import models

# Create your models here.
class Token(models.Model):
    emp_no = models.CharField(db_column='EMP_NO', max_length=20,primary_key=True)  # Field name made lowercase.
    token = models.CharField(max_length=500)
    deadline = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'TOKEN'

class AttendanceTable(models.Model):
    attend_id = models.CharField(db_column='ATTEND_ID', max_length=11)  # Field name made lowercase.
    attend_date = models.DateField(db_column='ATTEND_DATE')  # Field name made lowercase.
    attend_no = models.CharField(db_column='ATTEND_NO', primary_key=True, max_length=20)  # Field name made lowercase.
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)  # Field name made lowercase.
# Field name made lowercase.
    shift_no = models.CharField(db_column='SHIFT_NO', max_length=20)  
# Field name made lowercase.
    punch_in = models.DateTimeField(db_column='PUNCH_IN', blank=True, null=True)  # Field name made lowercase.
    punch_out = models.DateTimeField(db_column='PUNCH_OUT', blank=True, null=True)  # Field name made lowercase.
    in_position = models.CharField(db_column='IN_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    out_position = models.CharField(db_column='OUT_POSITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    overtime_no = models.CharField(db_column='OVERTIME_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    salary_no = models.CharField(db_column='SALARY_NO', max_length=20)  # Field name made lowercase.
    total_time = models.IntegerField(blank=True, null=True)
    fulltime = models.IntegerField(blank=True, null=True)
    latetime = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ATTENDANCE_TABLE'


class CompanyTable(models.Model):
    comp_id = models.CharField(db_column='COMP_ID', max_length=11)
    comp_no = models.CharField(db_column='COMP_NO', primary_key=True, max_length=20)
    comp_name = models.CharField(db_column='COMP_NAME', max_length=50)
    main = models.CharField(db_column='main', max_length=50)

    class Meta:
        managed = False
        db_table = 'COMPANY_TABLE'


class CompTimeTable(models.Model):
    # Field name made lowercase.
    comp_time_id = models.CharField(db_column='COMP_TIME_ID', max_length=11)
    # Field name made lowercase.
    comp_time_no = models.CharField(
        db_column='COMP_TIME_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    overtime_no = models.CharField(db_column='OVERTIME_NO', max_length=20)
    # Field name made lowercase.
    total = models.IntegerField(db_column='TOTAL')

    class Meta:
        managed = False
        db_table = 'COMP_TIME_TABLE'


class DepTable(models.Model):
    # Field name made lowercase.
    dep_no = models.IntegerField(db_column='DEP_NO', primary_key=True)
    # Field name made lowercase.
    dep_name = models.CharField(db_column='DEP_NAME', max_length=20)

    class Meta:
        managed = False
        db_table = 'DEP_TABLE'


class DetailsList(models.Model):
    # Field name made lowercase.
    details_id = models.CharField(db_column='DETAILS_ID', max_length=11)
    # Field name made lowercase.
    details_list = models.CharField(
        db_column='DETAILS_LIST', primary_key=True, max_length=20)
    # Field name made lowercase.
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)
    # Field name made lowercase.
    salary_no = models.CharField(db_column='SALARY_NO', max_length=20)
    # Field name made lowercase.
    salary = models.IntegerField(db_column='SALARY')
    # Field name made lowercase.
    overtime_pay = models.IntegerField(db_column='OVERTIME_PAY')

    class Meta:
        managed = False
        db_table = 'DETAILS_LIST'


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

class GroupTable(models.Model):
    # Field name made lowercase.
    group_no = models.CharField(
        db_column='GROUP_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    group_name = models.CharField(db_column='GROUP_NAME', max_length=50)

    class Meta:
        managed = False
        db_table = 'GROUP_TABLE'


class OvertimePay(models.Model):
    # Field name made lowercase.
    overtime_pay_id = models.CharField(db_column='OVERTIME_PAY_ID', max_length=11)
    # Field name made lowercase.
    overtime_pay_no = models.CharField(
        db_column='OVERTIME_PAY_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    salary_no = models.CharField(db_column='SALARY_NO', max_length=20)
    # Field name made lowercase.
    overtime_no = models.CharField(db_column='OVERTIME_NO', max_length=20)
    # Field name made lowercase.
    overtime_pay = models.IntegerField(db_column='OVERTIME_PAY')

    class Meta:
        managed = False
        db_table = 'OVERTIME_PAY'


class OvertimeType(models.Model):
    # Field name made lowercase.
    overtime_type_id = models.CharField(db_column='OVERTIME_TYPE_ID', max_length=11)
    # Field name made lowercase.
    overtime_type = models.IntegerField(
        db_column='OVERTIME_TYPE', primary_key=True)
    # Field name made lowercase.
    overtime_name = models.CharField(db_column='OVERTIME_NAME', max_length=20)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OVERTIME_TYPE'


class PunchTable(models.Model):
    # Field name made lowercase.
    punch_id = models.IntegerField(db_column='PUNCH_ID')
    # Field name made lowercase.
    punch_no = models.CharField(
        db_column='PUNCH_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)
    # Field name made lowercase.
    punch_record = models.IntegerField(db_column='PUNCH_RECORD')
    # Field name made lowercase.
    punch_date = models.DateTimeField(db_column='PUNCH_DATE')
    # Field name made lowercase.
    punch_name = models.CharField(db_column='PUNCH_NAME', max_length=20)
    # Field name made lowercase.
    punch_reason = models.TextField(db_column='PUNCH_REASON')

    class Meta:
        managed = False
        db_table = 'PUNCH_TABLE'


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


class SalaryTable(models.Model):
    # Field name made lowercase.
    salary_id = models.CharField(db_column='SALARY_ID', max_length=11)
    # Field name made lowercase.
    salary_no = models.CharField(
        db_column='SALARY_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    attend_no = models.CharField(db_column='ATTEND_NO', max_length=20)
    # Field name made lowercase.
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)
    # Field name made lowercase.
    details_list = models.CharField(db_column='DETAILS_LIST', max_length=20)
    # Field name made lowercase.
    overtime_pay_no = models.CharField(
        db_column='OVERTIME_PAY_NO', max_length=20)
    # Field name made lowercase.
    salary = models.IntegerField(db_column='SALARY')

    class Meta:
        managed = False
        db_table = 'SALARY_TABLE'


class ShiftsTable(models.Model):
    # shift_id = models.CharField(db_column='SHIFT_ID', max_length=11)  # 排班表流水號
    shift_no = models.CharField(
        db_column='SHIFT_NO', primary_key=True, max_length=20)  # 排班表編號
    attend_no = models.CharField(
        db_column='ATTEND_NO', max_length=20, blank=True, null=True)  # 出勤表編號
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)  # 員工編號
    date = models.DateField(db_column='DATE')  # 日期
    punch_in = models.DateTimeField(
        db_column='PUNCH_IN', blank=True, null=True, auto_now=False)  # 出勤時間 auto_now=True避免空值錯誤
    punch_out = models.DateTimeField(
        db_column='PUNCH_OUT', blank=True, null=True, auto_now=False)  # 下班時間 auto_now=True避免空值錯誤
    text = models.TextField(db_column='TEXT')  # 文字備註

    class Meta:
        managed = False
        db_table = 'SHIFTS_TABLE'


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

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

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
    working = models.CharField(db_column='WORKING', max_length=20)  # Field name made lowercase.
    in_addr=models.CharField(db_column='in_addr', max_length=555)  # Field name made lowercase.in_addr
    out_addr=models.CharField(db_column='out_addr', max_length=555)  # Field name made lowercase.in_addr

    class Meta:
        managed = False
        db_table = 'attendance_emp_view'

class ShiftsAttendanceEmpView(models.Model):
    attend_date = models.DateField(db_column='DATE')  # Field name made lowercase.
    attend_no = models.CharField(db_column='ATTEND_NO', primary_key=True, max_length=20)  # Field name made lowercase.
    shift_no = models.CharField(db_column='SHIFT_NO', max_length=20)  
    emp_no = models.CharField(db_column='EMP_NO', max_length=20)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', max_length=20)  # Field name made lowercase.
    group_no = models.CharField(db_column='GROUP_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    punch_in = models.DateTimeField(db_column='PUNCH_IN', blank=True, null=True)  # Field name made lowercase.
    punch_out = models.DateTimeField(db_column='PUNCH_OUT', blank=True, null=True)  # Field name made lowercase.
    s_punch_in = models.DateTimeField(db_column='s_punch_in', blank=True, null=True)  # Field name made lowercase.
    s_punch_out = models.DateTimeField(db_column='s_punch_out', blank=True, null=True)  # Field name made lowercase.
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
    working = models.CharField(db_column='WORKING', max_length=20)  # Field name made lowercase.
    in_addr=models.CharField(db_column='in_addr', max_length=555)  # Field name made lowercase.in_addr
    out_addr=models.CharField(db_column='out_addr', max_length=555)  # Field name made lowercase.in_addr

    class Meta:
        managed = False
        db_table = 'shifts_attendance_emp_view'

class AttendanceWorkOvertimeView(models.Model):  
    emp_no = models.CharField(db_column='emp_no', max_length=20)  # Field name made lowercase.
    emp_name= models.CharField(db_column='emp_name', max_length=20)  # Field name made lowercase.
    wp_name = models.CharField(db_column='wp_name', max_length=20)  # Field name made lowercase.
    group_name= models.CharField(db_column='group_name', max_length=20)  # Field name made lowercase.
    attend_date = models.DateField(db_column='attend_date')  # Field name made lowercase.
    st_punch_in = models.DateTimeField(db_column='ST_PUNCH_IN', blank=True, null=True)  # Field name made lowercase.
    st_punch_out = models.DateTimeField(db_column='ST_PUNCH_OUT', blank=True, null=True)  # Field name made lowercase.
    punch_in = models.DateTimeField(db_column='punch_in', blank=True, null=True)  # Field name made lowercase.
    punch_out = models.DateTimeField(db_column='punch_out', blank=True, null=True)  # Field name made lowercase.
    in_position = models.CharField(db_column='in_position', max_length=50, blank=True, null=True)  # Field name made lowercase.
    out_position = models.CharField(db_column='out_position', max_length=50, blank=True, null=True)  # Field name made lowercase.
    total_time = models.IntegerField(db_column='total_time',blank=True, null=True)
    latetime = models.IntegerField(db_column='latetime',blank=True, null=True)
    in_addr=models.CharField(db_column='in_addr', max_length=555)  # Field name made lowercase.in_addr
    out_addr=models.CharField(db_column='out_addr', max_length=555)  # Field name made lowercase.in_addr
    overtime_punch_in = models.DateTimeField(db_column='overtime_punch_in', blank=True, null=True)  # Field name made lowercase.
    overtime_punch_out = models.DateTimeField(db_column='overtime_punch_out', blank=True, null=True)  # Field name made lowercase.
    overtime_hours = models.IntegerField(db_column='overtime_hours')  # Field name made lowercase.
    start_time = models.DateTimeField(db_column='start_time', blank=True, null=True)  # Field name made lowercase.
    end_time = models.DateTimeField(db_column='end_time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'attendance_work_overtime_view'

class OvertimeEmpView(models.Model):
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
   #overtime_type_no = models.IntegerField(db_column='OVERTIME_TYPE_NO', blank=True, null=True)  # Field name made lowercase.
    #hours_change = models.IntegerField(db_column='HOURS_CHANGE', blank=True, null=True)  # Field name made lowercase.
    #disaster = models.IntegerField(db_column='DISASTER', blank=True, null=True)  # Field name made lowercase.
    #no_rest = models.IntegerField(db_column='NO_REST', blank=True, null=True)  # Field name made lowercase.
    dep_no = models.CharField(db_column='DEP_NO', max_length=20)  # Field name made lowercase.
    work_position = models.CharField(db_column='WORK_POSITION', max_length=20)  # Field name made lowercase.
    group_no= models.CharField(db_column='GROUP_NO', max_length=20)  # Field name made lowercase.
    emp_name= models.CharField(db_column='EMP_NAME', max_length=20)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'overtime_emp_view'
        unique_together = (('overtime_no', 'overtime_id'),)


class AttendanceEmpTodayView(models.Model):
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
    working = models.CharField(db_column='WORKING', max_length=20)  # Field name made lowercase.
   

    class Meta:
        managed = False
        db_table = 'attendance_emp_today_view'


class TimePeriod(models.Model):
    id = models.CharField(max_length=1,primary_key=True)
    starttime = models.TimeField(db_column='startTime', max_length=20)  # Field name made lowercase.
    endtime = models.TimeField(db_column='endTime', max_length=20)  # Field name made lowercase.
    crossday= models.CharField(db_column='crossDay', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TIME_PERIOD'


class WorkpositionList(models.Model):
    wp_name = models.CharField(db_column='WP_name', max_length=1)  # Field name made lowercase.
    wp_code = models.CharField(db_column='WP_code', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'workPosition_list'