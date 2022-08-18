# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AttendanceTable(models.Model):

    # Field name made lowercase.

    # Field name made lowercase.
    attend_no = models.CharField(
        db_column='ATTEND_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    # comp_no = models.ForeignKey(
    #     'CompanyTable', models.DO_NOTHING, db_column='COMP_NO')
    # Field name made lowercase.
    rest_no = models.ForeignKey(
        'RestTable', models.DO_NOTHING, db_column='REST_NO')
    # Field name made lowercase.
    comp_time_no = models.ForeignKey(
        'CompTimeTable', models.DO_NOTHING, db_column='COMP_TIME_NO')
    # Field name made lowercase.
    salary_no = models.ForeignKey(
        'SalaryTable', models.DO_NOTHING, db_column='SALARY_NO')
    # Field name made lowercase.
    record = models.CharField(db_column='RECORD', max_length=20)
    # Field name made lowercase.
    position = models.CharField(db_column='POSITION', max_length=50)
    # Field name made lowercase.
    attend_date = models.DateTimeField(db_column='ATTEND_DATE')

    class Meta:
        managed = False
        db_table = 'ATTENDANCE_TABLE'





class CompTimeTable(models.Model):
    # Field name made lowercase.

    # Field name made lowercase.
    comp_time_no = models.CharField(
        db_column='COMP_TIME_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    overtime_no = models.ForeignKey(
        'WorkOvertime', models.DO_NOTHING, db_column='OVERTIME_NO')
    # Field name made lowercase.
    attend_no = models.ForeignKey(
        AttendanceTable, models.DO_NOTHING, db_column='ATTEND_NO')
    # Field name made lowercase.
    total = models.IntegerField(db_column='TOTAL')

    class Meta:
        managed = False
        db_table = 'COMP_TIME_TABLE'


class DetailsList(models.Model):
    # Field name made lowercase.

    # Field name made lowercase.
    details_list = models.CharField(
        db_column='DETAILS_LIST', primary_key=True, max_length=20)
    # Field name made lowercase.
    # emp_no = models.ForeignKey(
    #     'EmpTable', models.DO_NOTHING, db_column='EMP_NO')
    # Field name made lowercase.
    salary_no = models.ForeignKey(
        'SalaryTable', models.DO_NOTHING, db_column='SALARY_NO')
    # Field name made lowercase.
    salary = models.IntegerField(db_column='SALARY')
    # Field name made lowercase.
    overtime_pay = models.IntegerField(db_column='OVERTIME_PAY')

    class Meta:
        managed = False
        db_table = 'DETAILS_LIST'


class OvertimePay(models.Model):
    # Field name made lowercase.

    # Field name made lowercase.
    overtime_pay_no = models.CharField(
        db_column='OVERTIME_PAY_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    salary_no = models.ForeignKey(
        'SalaryTable', models.DO_NOTHING, db_column='SALARY_NO')
    # Field name made lowercase.
    overtime_no = models.ForeignKey(
        'WorkOvertime', models.DO_NOTHING, db_column='OVERTIME_NO')
    # Field name made lowercase.
    overtime_pay = models.IntegerField(db_column='OVERTIME_PAY')

    class Meta:
        managed = False
        db_table = 'OVERTIME_PAY'


class OvertimeType(models.Model):
    # Field name made lowercase.

    # Field name made lowercase.
    overtime_type = models.IntegerField(
        db_column='OVERTIME_TYPE', primary_key=True)
    # Field name made lowercase.
    overtime_no = models.ForeignKey(
        'WorkOvertime', models.DO_NOTHING, db_column='OVERTIME_NO')
    # Field name made lowercase.
    overtime_name = models.CharField(db_column='OVERTIME_NAME', max_length=20)

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
    # comp_no = models.ForeignKey(
    #     CompanyTable, models.DO_NOTHING, db_column='COMP_NO')
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
    # Field name made lowercase.

    # Field name made lowercase.
    rest_no = models.CharField(
        db_column='REST_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    attend_no = models.ForeignKey(
        AttendanceTable, models.DO_NOTHING, db_column='ATTEND_NO')
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


class RestType(models.Model):
    # Field name made lowercase.

    # Field name made lowercase.
    rest_type_no = models.IntegerField(
        db_column='REST_TYPE_NO', primary_key=True)
    # Field name made lowercase.
    rest_no = models.ForeignKey(
        RestTable, models.DO_NOTHING, db_column='REST_NO')
    # Field name made lowercase.
    type_name = models.CharField(db_column='TYPE_NAME', max_length=20)

    class Meta:
        managed = False
        db_table = 'REST_TYPE'


class SalaryTable(models.Model):

    # Field name made lowercase.
    salary_no = models.CharField(
        db_column='SALARY_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    attend_no = models.ForeignKey(
        AttendanceTable, models.DO_NOTHING, db_column='ATTEND_NO')
    # Field name made lowercase.
    details_list = models.ForeignKey(
        DetailsList, models.DO_NOTHING, db_column='DETAILS_LIST')
    # Field name made lowercase.
    overtime_pay_no = models.ForeignKey(
        OvertimePay, models.DO_NOTHING, db_column='OVERTIME_PAY_NO')
    # Field name made lowercase.
    salary = models.IntegerField(db_column='SALARY')

    class Meta:
        managed = False
        db_table = 'SALARY_TABLE'


class WorkOvertime(models.Model):
    # Field name made lowercase.

    # Field name made lowercase.
    overtime_no = models.CharField(
        db_column='OVERTIME_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    comp_time_no = models.ForeignKey(
        CompTimeTable, models.DO_NOTHING, db_column='COMP_TIME_NO')
    # Field name made lowercase.
    overtime_pay_no = models.ForeignKey(
        OvertimePay, models.DO_NOTHING, db_column='OVERTIME_PAY_NO')
    # Field name made lowercase.
    overtime_date = models.DateField(db_column='OVERTIME_DATE')
    # Field name made lowercase.
    overtime_hours = models.IntegerField(db_column='OVERTIME_HOURS')
    # Field name made lowercase.
    hours_change = models.IntegerField(db_column='HOURS_CHANGE')
    # Field name made lowercase.
    disaster = models.IntegerField(db_column='DISASTER')
    # Field name made lowercase.
    no_rest = models.IntegerField(db_column='NO_REST')

    class Meta:
        managed = False
        db_table = 'WORK_OVERTIME'


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


class ZzWorkOvertime(models.Model):

    overtime_no = models.CharField(
        db_column='OVERTIME_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    attend_no = models.CharField(
        db_column='ATTEND_NO',  max_length=20)
    # Field name made lowercase.
    overtime_pay_no = models.CharField(
        db_column='OVERTIME_PAY_NO', max_length=20)
    # Field name made lowercase.
    overtime_date = models.DateField(db_column='OVERTIME_DATE')
    # Field name made lowercase.
    overtime_hours = models.IntegerField(
        db_column='OVERTIME_HOURS', default='0')
    overtime_check = models.IntegerField(
        db_column='OVERTIME_CHECK', default='0')
    punch_in = models.DateTimeField(db_column='PUNCH_IN')
    punch_out = models.DateTimeField(db_column='PUNCH_OUT')
    emp_no = models.CharField(db_column='EMP_NO',  max_length=20)
    endtime=models.TimeField(db_column='endtime')
    starttime=models.TimeField(db_column='starttime')

    class Meta:
        managed = False
        db_table = 'WORK_OVERTIME'

class GroupTable(models.Model):

    group_no = models.CharField(
        db_column='GROUP_NO', max_length=20,primary_key=True)

    group_name=models.CharField(db_column='GROUP_NAME',max_length=20)
    class Meta:
        managed = False
        db_table = 'GROUP_TABLE'


class ZzEmpTable(models.Model):

    emp_no = models.CharField(
        db_column='EMP_NO', primary_key=True, max_length=20, db_collation='utf8_general_ci', unique=True)

    emp_name = models.CharField(
        db_column='EMP_NAME', max_length=20, db_collation='utf8_general_ci')

    dep_no = models.CharField(
        db_column='DEP_NO', max_length=20, db_collation='utf8_general_ci')

    comp_no = models.CharField(
        db_column='COMP_NO', max_length=20)
    user_pwd = models.CharField(
        db_column='USER_PWD', max_length=20, db_collation='utf8_general_ci')
    line_id = models.CharField(
        db_column='line_id', max_length=50, db_collation='utf8_general_ci')
    tel = models.CharField(max_length=10)


    group_no = models.ForeignKey(GroupTable,models.DO_NOTHING,'GROUP_NO', blank=True, null=True, db_column="GROUP_NO",to_field="group_no")
    group_leader = models.IntegerField(
        db_column='GROUP_leader', default='0')
    # group_name=models.ForeignKey()
    class Meta:
        managed = False
        db_table = 'EMP_TABLE'


class ZzAttendanceTable(models.Model):

    attend_no = models.CharField(
        db_column='ATTEND_NO', primary_key=True, max_length=20)

    overtime_no = models.CharField(
        db_column='OVERTIME_NO', max_length=50)
    shift_no = models.CharField(
        db_column='SHIFT_NO', max_length=20)  # 排班表編號
    salary_no = models.CharField(
        db_column='SALARY_NO', max_length=50)
    # Field name made lowercase.
    punch_in = models.DateTimeField(db_column='PUNCH_IN')
    punch_out = models.DateTimeField(db_column='PUNCH_OUT')

    in_position = models.CharField(db_column='IN_POSITION', max_length=50)
    out_position = models.CharField(db_column='OUT_POSITION', max_length=50)

    attend_date = models.DateField(db_column='ATTEND_DATE')
    emp_no = models.CharField(
        db_column='EMP_NO', max_length=20)
    latetime = models.IntegerField(
        db_column='latetime')
    fulltime = models.IntegerField(
        db_column='fulltime')
    total_time = models.IntegerField(
        db_column='total_time')


    # ZzEmpTable = models.ForeignKey('ZzEmpTable', on_delete=models.DO_NOTHING, null=True, related_name='ZzEmpTable',
    #                                to_field='emp_no', blank=True)
    class Meta:
        managed = False
        db_table = 'ATTENDANCE_TABLE'


class CompanyTable(models.Model):

    comp_no = models.CharField(
        db_column='COMP_NO', primary_key=True, max_length=20)

    comp_name = models.CharField(db_column='COMP_NAME', max_length=50)
    main = models.IntegerField(db_column='main')

    class Meta:
        managed = False
        db_table = 'COMPANY_TABLE'

class ShiftsTable(models.Model):
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

class overtime_check_view(models.Model):
    attend_no = models.CharField(
        db_column='ATTEND_NO', primary_key=True, max_length=20)
    overtime_no = models.CharField(
        db_column='OVERTIME_NO', max_length=50)
    attend_date = models.DateField(db_column='ATTEND_DATE')
    overtime_check = models.IntegerField(
        db_column='OVERTIME_CHECK')

    emp_no = models.CharField(
        db_column='EMP_NO', max_length=20)
    tel = models.CharField(max_length=10)
    emp_name = models.CharField(
        db_column='EMP_NAME', max_length=20)
    group_no = models.CharField(
        db_column='GROUP_NO', max_length=20)
    group_name = models.CharField(
        db_column='GROUP_NAME', max_length=20)
    group_leader = models.IntegerField(
        db_column='GROUP_leader')
    class Meta:
        managed = False
        db_table = 'overtime_check_view'


class second_EmpTable(models.Model):

    emp_no = models.CharField(
        db_column='EMP_NO', primary_key=True, max_length=20, db_collation='utf8_general_ci', unique=True)

    emp_name = models.CharField(
        db_column='EMP_NAME', max_length=20, db_collation='utf8_general_ci')

    dep_no = models.CharField(
        db_column='DEP_NO', max_length=20, db_collation='utf8_general_ci')

    comp_no = models.CharField(
        db_column='COMP_NO', max_length=20)
    user_pwd = models.CharField(
        db_column='USER_PWD', max_length=20, db_collation='utf8_general_ci')
    line_id = models.CharField(
        db_column='line_id', max_length=50, db_collation='utf8_general_ci')
    tel = models.CharField(max_length=10)


    group_no = models.ForeignKey(GroupTable,models.DO_NOTHING,'GROUP_NO', blank=True, null=True, db_column="GROUP_NO",to_field="group_no")
    group_leader = models.IntegerField(
        db_column='GROUP_leader', default='0')
    # group_name=models.ForeignKey()
    class Meta:
        app_label='HRCS_test'
        managed = False
        db_table = 'EMP_TABLE'

class second_WorkOvertime(models.Model):

    overtime_no = models.CharField(
        db_column='OVERTIME_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    attend_no = models.CharField(
        db_column='ATTEND_NO',  max_length=20)
    # Field name made lowercase.
    overtime_pay_no = models.CharField(
        db_column='OVERTIME_PAY_NO', max_length=20)
    # Field name made lowercase.
    overtime_date = models.DateField(db_column='OVERTIME_DATE')
    # Field name made lowercase.
    overtime_hours = models.IntegerField(
        db_column='OVERTIME_HOURS', default='0')
    overtime_check = models.IntegerField(
        db_column='OVERTIME_CHECK', default='0')
    punch_in = models.DateTimeField(db_column='PUNCH_IN')
    punch_out = models.DateTimeField(db_column='PUNCH_OUT')
    emp_no = models.CharField(db_column='EMP_NO',  max_length=20)

    class Meta:
        app_label = 'HRCS_test'
        managed = False
        db_table = 'WORK_OVERTIME'