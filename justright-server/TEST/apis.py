from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
import json
from TEST.models import ZzEmpTable  # 從test的model抓取ZzEmpTable這個class(資料表)
from TEST.models import ShiftsTable
from TEST.models import AttendanceTable
from TEST.models import RestTable
from TEST.models import EmpTable
from TEST.models import JwtToken
from TEST.models import Token
from TEST.models import AttendanceEmpView
from TEST.models import WorkOvertime

from django.db.models import Q
#from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime as dt, timedelta, timezone
import datetime
import jwt
import secrets
from django.core.mail import send_mail

status = ''
@csrf_exempt
def getWorkovertime(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_work_overtime(request)})
@csrf_exempt
def getEmpdata(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_emp_data(request)})
    if request.method == 'POST':
        return JsonResponse({'status': _insert_emp_data(request)})
    if request.method == 'PUT':
        return JsonResponse({'status': _update_emp_data(request)})

@csrf_exempt
def getAttendanceEmpViewdata(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_attendance_emp_viwe_data(request)})
@csrf_exempt
def login(request: WSGIRequest):  # 登入測試
    if request.method == 'POST':
        return JsonResponse({'response': _login(request)})
@csrf_exempt
def post(request: WSGIRequest): 
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'status': 'Get posts succeed', 'ZzEmpTable': _get_all_posts()})
@csrf_exempt
def ForgetPassword(request: WSGIRequest):
    if request.method == 'POST':
        return JsonResponse({'status': _forget_password(request)})
    else:
        return JsonResponse({'status': 'error'})
def _verify_jwt(token):
    verify=JwtToken.objects.filter(token=token)
    try:
        nowtime = dt.strptime(str(dt.now().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
        exp_time=dt.strptime(str(verify[0].exp_time.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
        print('AAA')
        if nowtime-exp_time>timedelta(seconds=0):
            print('AAAA')
            raise Exception("over limit!")
        print(nowtime-exp_time)
    except Exception as e:
        print(e)
        return e

@csrf_exempt
def ResetPassword(request: WSGIRequest):
    if request.method == 'POST':
        return JsonResponse({'status': _reset_password(request)})
    else:
        return JsonResponse({'status': 'error'})


@csrf_exempt
def testShiftdata(request: WSGIRequest):
    if request.method == 'GET':
        return JsonResponse({'Data': _get_shifts_data(request)})
    if request.method == 'POST':
        return JsonResponse({'status': _insert_shifts_data(request)})
    if request.method == 'PUT':
        return JsonResponse({'status': _update_Shift_data(request)})


@csrf_exempt
def getAttendancedata(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_attendance_data(request)})


@csrf_exempt
def getRestdata(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'status': 'Get posts succeed', 'RestTable': _get_rest_data()})
    if request.method == 'POST':
        return JsonResponse({'status': _update_rest_data(request)})



import requests

def _login(request):
    requestBody = request.body
    requestData = json.loads(requestBody)
    username =  requestData['username']
    password = requestData['password']
    print(username)
    my_data = {'username':username, 'password': password}
    errorMsg='error!'
    posts = []
    try:
        filter_post = EmpTable.objects.filter(Q(emp_no=username) & Q(user_pwd=password))
        payload = {
        'iss': 'example.com',#改
        'sub': filter_post[0].emp_name,
        'aud': 'www.example.com',#改
        'exp': dt.utcnow(),   # must use UTC time 過期時間 應該會改
        'nbf': dt.utcnow(),
        'iat': dt.utcnow(),
        'jti': 'unique_jwt_id',#改?
        'username': filter_post[0].emp_name,
        'password':filter_post[0].user_pwd
        }
        token=jwt.encode(payload, 'secret', algorithm='HS256')
        print(token)
        #理論上來說token是要解碼之後再跟後端資料庫進行比對了 不過這邊容後再做
        exp_time=(dt.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        print(exp_time)
        created = JwtToken.objects.get_or_create(username=username)
        if created:
            print('aa')
            _post =  JwtToken.objects.filter(username=username)
            _post.update(
            token=token,
            exp_time=exp_time
            )   
        else:
            print('aaa')
            JwtToken.objects.create(
                username=username,
                token=token,
                exp_time=exp_time
            )
        # person just refers to the existing one
        post_data={
                'username':filter_post[0].emp_no,
                'token':token
        }
        posts.append(post_data)

        return posts

    except Exception as e:
        if 'list index out of range' in str(e):
            errorMsg += '請重新確認輸入內容!'
        else:
            errorMsg += str(e)
        return errorMsg

def _get_all_posts():
    # all posts
    all_posts = ZzEmpTable.objects.all()  # 把TEST.models裡ZzEmpTable所擁有的東西都弄出來

    posts = []

    for _post in all_posts:
        post_data = {  # 按照api格式塞進去
            'emp_no': _post.emp_no,
        }
        posts.append(post_data)

    return posts


def _get_shifts_data(request):
    attend_no = request.GET.get('attend_no')
    shift_no = request.GET.get('shift_no')
    emp_no = request.GET.get('emp_no')
    all_posts = ShiftsTable.objects.all()  # 自模型取出資料
    filter_post = []
    posts = []
    errorMsg = 'ERROR!'

    # print('_get_shifts_data','attend_no',attend_no,'shift_no',shift_no,'emp_no',emp_no)

    if attend_no != None:
        try:
            filter_post = ShiftsTable.objects.filter(attend_no=attend_no)
            for _post in filter_post:  # 按照api格式塞進去
                post_data = {
                    'shift_no': _post.shift_no,
                    'attend_no': _post.attend_no,
                    'group_no': _post.group_no,
                    'emp_no': _post.emp_no,
                    'date': _post.date,
                    'punch_in': _post.punch_in,
                    'punch_out': _post.punch_out,
                }

                posts.append(post_data)
            return posts
        except:
            return errorMsg

    elif shift_no != None:
        try:
            filter_post = ShiftsTable.objects.filter(shift_no=shift_no)
            for _post in filter_post:  # 按照api格式塞進去
                post_data = {
                    'shift_no': _post.shift_no,
                    'attend_no': _post.attend_no,
                    'group_no': _post.group_no,
                    'emp_no': _post.emp_no,
                    'date': _post.date,
                    'punch_in': _post.punch_in,
                    'punch_out': _post.punch_out,
                }

                posts.append(post_data)
            return posts
        except:
            return errorMsg

    elif emp_no != None:
        try:
            filter_post = ShiftsTable.objects.filter(emp_no=emp_no)
            for _post in filter_post:  # 按照api格式塞進去
                post_data = {
                    'shift_no': _post.shift_no,
                    'attend_no': _post.attend_no,
                    'group_no': _post.group_no,
                    'emp_no': _post.emp_no,
                    'date': _post.date,
                    'punch_in': _post.punch_in,
                    'punch_out': _post.punch_out,
                }

                posts.append(post_data)
            return posts
        except:
            return errorMsg

    else:
        for _post in all_posts:  # 按照api格式塞進去
            post_data = {
                'shift_no': _post.shift_no,
                'attend_no': _post.attend_no,
                'group_no': _post.group_no,
                'emp_no': _post.emp_no,
                'date': _post.date,
                'punch_in': _post.punch_in,
                'punch_out': _post.punch_out,
            }

            posts.append(post_data)
        return posts


def _update_Shift_data(request):
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'

    try:
        _post = ShiftsTable.objects.filter(shift_no=requestData['shift_no'])
        _post.update(
            attend_no=requestData['attend_no'],
            group_no=requestData['group_no'],
            date=requestData['date'],
            punch_in=requestData['punch_in'],
            punch_out=requestData['punch_out']
        )
    except Exception as e:
        return errorMsg

    return 'succeed'


def _update_rest_data(request):  # 修改範例
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'

    try:
        # 近似select * from RestTable where rest_id=$_REQUEST['rest_id']
        _post = RestTable.objects.filter(rest_id=requestData['rest_id'])
        _post.update(rest_reason=requestData['rest_reason'])  # UPDATE(ry
    except Exception as e:  # 我還沒管 之後再處理
        return errorMsg

    return 'succeed'


def _insert_shifts_data(request):
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = 'ERROR!'

    try:
        newShiftdata = ShiftsTable.objects.create(
            shift_no=requestData['shift_no'],
            emp_no=requestData['emp_no'],
            date=requestData['date'],
            punch_in=requestData['punch_in'],
            punch_out=requestData['punch_out'],
            text=requestData['text'])
    except Exception as e:
        if 'Duplicate entry' in str(e):
            errorMsg += '該編號重複，請再確認編號'
        else:
            errorMsg += str(e)
        return errorMsg

    return 'Succeed'


def _get_attendance_data(request):  # 出勤管理 基礎頁面
    requestBody = request.body
    requestData = json.loads(requestBody)
    try:
        all_posts = AttendanceTable.objects.filter(Q(emp_no=requestData['emp_no']) & Q(
            attend_date__year=requestData['year']) & Q(attend_date__month=requestData['month']))  # 自模型取出資料

        posts = []

        for _post in all_posts:  # 按照api格式塞進去
            post_data = {  # 按照api格式塞進去
                'emp_no': _post.emp_no,
                'punch_in': _post.punch_in,
                'punch_out': _post.punch_out,
                'in_position': _post.in_position,
                'out_position': _post.out_position,
                'total_time': _post.total_time,
                'fulltime': _post.fulltime,
                'latetime': _post.latetime
            }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
        return Response

def _insert_emp_data(request):
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = 'ERROR!'

    try:
        newEmpdata = EmpTable.objects.create(
            emp_no=requestData['emp_no'],
            emp_name=requestData['emp_name'],
            comp_no=requestData['comp_no'],
            dep_no=requestData['dep_no'],
            work_position=requestData['work_position'],
            user_pwd=requestData['user_pwd'],
            tel=requestData['tel'],
            group_no=requestData['group_no'],
            group_leader=requestData['group_leader'],
            working=requestData['working'],
            auth=requestData['auth'],
            mail=requestData['mail']

        )
    except Exception as e:
        if 'Duplicate entry' in str(e):
            errorMsg += '該編號重複，請再確認編號'
        else:
            errorMsg += str(e)
        return errorMsg

    return 'Succeed'
def _get_rest_data():
    all_posts = RestTable.objects.all()  # 自模型取出資料

    posts = []

    for _post in all_posts:  # 按照api格式塞進去
        post_data = {  # 按照api格式塞進去
            'rest_id': _post.rest_id,
            'rest_no': _post.rest_no,
            'attend_no': _post.attend_no,
            'rest_type': _post.rest_type,
            'app_date': _post.app_date,
            'rest_date': _post.rest_date,
            'rest_reason': _post.rest_reason
        }
        posts.append(post_data)

    return posts


def _reset_password(request):  # 忘記密碼重設請求
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改失敗!'
    # print("in")
    try:
        _post = EmpTable.objects.filter(emp_no=requestData['emp_no'])
        _token= Token.objects.filter(emp_no=requestData['emp_no'])
        nowtime = datetime.strptime(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
        deadline=datetime.strptime(str(_token[0].deadline.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
        print(nowtime)
        print(deadline)
        if _token[0].token==requestData['token'] and nowtime-deadline<timedelta(seconds=0):#token正確且時間在deadline錢
            _post.update(user_pwd=requestData['password'])  # UPDATE(ry
            _token.delete()
            print("yes")
        else:
            print("no") 

        #_post.update(user_pwd=requestData['password'])  # UPDATE(ry
    except Exception as e:
        if 'list index out of range' in str(e):
            errorMsg += '查無此帳號!請重新確認輸入內容!'
        else:
            errorMsg += str(e)
        return errorMsg

    return 'succeed'

def _forget_password(request):#忘記密碼驗證&寄出驗證信
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '驗證失敗!'
    # print("in")
    try:
        _post = EmpTable.objects.filter(Q(emp_no=requestData['emp_no']) & Q(mail=requestData['mail']))
        email=_post[0].mail#確保是使用者的信箱
        deadline=requestData['deadline']
        token=secrets.token_urlsafe(20)#產生亂數token
        Token.objects.create(#紀錄重置密碼的token
            emp_no=requestData['emp_no'],
            token=token,
            deadline=deadline
        )
        print(token)
        send_mail('From django', '驗證的前端連結+/'+token, 'cgptiot@gmail.com', [email])
        #標題.內容.寄信者的信箱.收信者的信箱


        print("發送成功!")
    except Exception as e:
        if 'list index out of range' in str(e):
            errorMsg += '帳號或信箱輸入錯誤!請重新確認輸入內容!'
        else:
            errorMsg += str(e)
        return errorMsg

    return 'succeed'
def _get_emp_data(request):  # 員工
    try:
        jwt_verify=_verify_jwt(request.headers['Token'])
        if "list index out of range" in str(jwt_verify):
            raise Exception("token不存在!")
        elif "over limit!" in str(jwt_verify):
            raise Exception("token已過期!")

        all_posts = EmpTable.objects.all()
        posts = []

        for _post in all_posts:  # 按照api格式塞進去
            post_data = {  # 按照api格式塞進去
            'emp_no':_post.emp_no,
            'emp_name':_post.emp_name,
            'comp_no':_post.comp_no,
            'dep_no':_post.dep_no,
            'work_position':_post.work_position,
            'tel':_post.tel,
            'group_no':_post.group_no,
            'group_leader':_post.group_leader,
            'working':_post.working,
            'mail':_post.mail
            }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
    return Response

def _update_emp_data(request):
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'
    try:
        if requestData['working']!=None:#如果把working傳了過來 代表是員工離職了 改working
            _post = EmpTable.objects.filter(emp_no=requestData['emp_no'])
            _post.update(
                working=requestData['working'],
            )
    except Exception as e:
        if 'working' in str(e):
            try:
                _post = EmpTable.objects.filter(emp_no=requestData['emp_no'])
                _post.update(
                    emp_name=requestData['emp_name'],
                    comp_no=requestData['comp_no'],
                    dep_no=requestData['dep_no'],
                    work_position=requestData['work_position'],
                    tel=requestData['tel'],
                    group_no=requestData['group_no'],
                    group_leader=requestData['group_leader']
                )
            except Exception as e:
                errorMsg += str(e)
                return errorMsg
        else:
            errorMsg += str(e)
            return errorMsg
    return 'succeed'


def _get_work_overtime(request):
    emp_no = request.GET.get('emp_no')
    start_date= request.GET.get('start_date')
    end_date=request.GET.get('end_date')

    if emp_no!=None and start_date!=None and end_date!=None:
        #try:
        all_posts = WorkOvertime.objects.filter(Q(emp_no=emp_no) 
        & Q(overtime_date__range=(start_date,end_date)))  # 自模型取出資料
        print(all_posts)
        posts = []
        for _post in all_posts:  # 按照api格式塞進去
            punch_in="Null" if _post.punch_in==None else _post.punch_in.strftime("%Y-%m-%d %H:%M:%S")#三元運算子
            punch_out="Null" if _post.punch_out==None else _post.punch_out.strftime("%Y-%m-%d %H:%M:%S")
            post_data = {  # 按照api格式塞進去
                'overtime_id':_post.overtime_id, 
                'overtime_no':_post.overtime_no,
                'attend_no':_post.attend_no,
                'overtime_pay_no':_post.overtime_pay_no,
                'overtime_date':_post.overtime_date,
                'emp_no':_post.emp_no,
                'punch_in':punch_in,
                'punch_out':punch_out,
                'overtime_hours':_post.overtime_hours,
                'overtime_check':_post.overtime_check,
                'overtime_type_no':_post.overtime_type_no,
                'hours_change':_post.hours_change,
                'disaster':_post.disaster,
                'no_rest':_post.no_rest
            }
            posts.append(post_data)

        if posts == []:
            Response = {
                    'status': 'Null',
                    'data': posts
            }
        else:
            Response = {
                    'status': 'Succeed',
                    'data': posts
            }
        return Response
    else:
        Response = {
            'status': 'succeed',
            'msg': '查無資料'
        }
def _get_attendance_emp_viwe_data(request):  # 取得出勤管理 基礎頁面的資料 需求emp_no,year,month
    try:
        jwt_verify=_verify_jwt(request.headers['Token'])
        if "list index out of range" in str(jwt_verify):
            raise Exception("token不存在!")
        elif "over limit!" in str(jwt_verify):
            raise Exception("token已過期!")
    except Exception as e:
        Response = {
                'status': 'Error',
                'msg': str(e)
            }
        return Response
    status = ''
    Response = {}
    emp_no = request.GET.get('emp_no')
    year = request.GET.get('year')
    month = request.GET.get('month')
    day=request.GET.get('day')
    if emp_no!= None and year!=None and month!=None and day!=None: 
        try:
            all_posts = AttendanceEmpView.objects.filter(Q(emp_no=request.GET.get('emp_no')) & 
            Q(attend_date__year=request.GET.get('year')) & Q(attend_date__month=request.GET.get('month')) & Q(attend_date__day=request.GET.get('day'))
            )  # 自模型取出資料
            posts = []

            for _post in all_posts:  # 按照api格式塞進去
                punch_in=None if _post.punch_in==None else _post.punch_in.strftime("%Y-%m-%d %H:%M:%S")#三元運算子
                punch_out=None if _post.punch_out==None else _post.punch_out.strftime("%Y-%m-%d %H:%M:%S")
                if _post.group_no!=0 and _post.group_no!="0":
                    post_data = {  # 按照api格式塞進去
                        'attend_no':_post.attend_no,
                        'attend_date':_post.attend_date,
                        'comp_name':_post.comp_name,
                        'shift_no':_post.shift_no,
                        'emp_no': _post.emp_no,
                        'emp_name':_post.emp_name,
                        'group_no':_post.group_no,
                        'punch_in':punch_in,
                        'punch_out':punch_out,
                        'in_position':_post.in_position,
                        'out_position':_post.out_position,
                        'overtime_no':_post.overtime_no,
                        'salary_no':_post.salary_no,
                        'total_time':_post.total_time,
                        'fulltime':_post.fulltime,
                        'latetime':_post.latetime,
                        'attend_id':_post.attend_id,
                        'tel':_post.tel,
                        'work_position':_post.work_position

                    }
                    posts.append(post_data)

            if posts == []:
                Response = {
                    'status': 'Null',
                    'data': posts
                }
            else:
                Response = {
                    'status': 'Succeed',
                    'data': posts
                }
            #return Response
        except Exception as e:
            Response = {
                'status': 'Error',
                'msg': str(e)
            }
    elif  emp_no!= None and year!=None and month!=None: 
        try:
            all_posts = AttendanceEmpView.objects.filter(Q(emp_no=request.GET.get('emp_no')) & Q(attend_date__year=request.GET.get('year')) & Q(attend_date__month=request.GET.get('month')))  # 自模型取出資料
            posts = []

            for _post in all_posts:  # 按照api格式塞進去
                punch_in=None if _post.punch_in==None else _post.punch_in.strftime("%Y-%m-%d %H:%M:%S")#三元運算子
                punch_out=None if _post.punch_out==None else _post.punch_out.strftime("%Y-%m-%d %H:%M:%S")
                if _post.group_no!=0 and _post.group_no!="0":
                    post_data = {  # 按照api格式塞進去
                        'attend_no':_post.attend_no,
                        'attend_date':_post.attend_date,
                        'comp_name':_post.comp_name,
                        'shift_no':_post.shift_no,
                        'emp_no': _post.emp_no,
                        'emp_name':_post.emp_name,
                        'group_no':_post.group_no,
                        'punch_in':punch_in,
                        'punch_out':punch_out,
                        'in_position':_post.in_position,
                        'out_position':_post.out_position,
                        'overtime_no':_post.overtime_no,
                        'salary_no':_post.salary_no,
                        'total_time':_post.total_time,
                        'fulltime':_post.fulltime,
                        'latetime':_post.latetime,
                        'attend_id':_post.attend_id,
                        'tel':_post.tel,
                        'work_position':_post.work_position
                    }
                    posts.append(post_data)

            if posts == []:
                Response = {
                    'status': 'Null',
                    'data': posts
                }
            else:
                Response = {
                    'status': 'Succeed',
                    'data': posts
                }
            #return Response
        except Exception as e:
            Response = {
                'status': 'Error',
                'msg': str(e)
            }
    elif  year!=None and month!=None and day!=None: 
        try:
            all_posts = AttendanceEmpView.objects.filter(Q(attend_date__year=request.GET.get('year')) & Q(attend_date__month=request.GET.get('month')) & Q(attend_date__day=request.GET.get('day')))  # 自模型取出資料
            posts = []

            for _post in all_posts:  # 按照api格式塞進去
                punch_in=None if _post.punch_in==None else _post.punch_in.strftime("%Y-%m-%d %H:%M:%S")#三元運算子
                punch_out=None if _post.punch_out==None else _post.punch_out.strftime("%Y-%m-%d %H:%M:%S")
                if _post.group_no!=0 and _post.group_no!="0":
                    post_data = {  # 按照api格式塞進去
                        'attend_no':_post.attend_no,
                        'attend_date':_post.attend_date,
                        'comp_name':_post.comp_name,
                        'shift_no':_post.shift_no,
                        'emp_no': _post.emp_no,
                        'emp_name':_post.emp_name,
                        'group_no':_post.group_no,
                        'punch_in':punch_in,
                        'punch_out':punch_out,
                        'in_position':_post.in_position,
                        'out_position':_post.out_position,
                        'overtime_no':_post.overtime_no,
                        'salary_no':_post.salary_no,
                        'total_time':_post.total_time,
                        'fulltime':_post.fulltime,
                        'latetime':_post.latetime,
                        'attend_id':_post.attend_id,
                        'tel':_post.tel,
                        'work_position':_post.work_position

                    }
                    posts.append(post_data)

            if posts == []:
                Response = {
                    'status': 'Null',
                    'data': posts
                }
            else:
                Response = {
                    'status': 'Succeed',
                    'data': posts
                }
            #return Response
        except Exception as e:
            Response = {
                'status': 'Error',
                'msg': str(e)
            }     
    elif  year!=None and month!=None: 
        try:
            all_posts = AttendanceEmpView.objects.filter(Q(attend_date__year=request.GET.get('year')) & Q(attend_date__month=request.GET.get('month')) )  # 自模型取出資料
            posts = []

            for _post in all_posts:  # 按照api格式塞進去
                punch_in=None if _post.punch_in==None else _post.punch_in.strftime("%Y-%m-%d %H:%M:%S")#三元運算子
                punch_out=None if _post.punch_out==None else _post.punch_out.strftime("%Y-%m-%d %H:%M:%S")
                if _post.group_no!=0 and _post.group_no!="0":
                    post_data = {  # 按照api格式塞進去
                        'attend_no':_post.attend_no,
                        'attend_date':_post.attend_date,
                        'comp_name':_post.comp_name,                    
                        'shift_no':_post.shift_no,
                        'emp_no': _post.emp_no,
                        'emp_name':_post.emp_name,
                        'group_no':_post.group_no,
                        'punch_in':punch_in,
                        'punch_out':punch_out,
                        'in_position':_post.in_position,
                        'out_position':_post.out_position,
                        'overtime_no':_post.overtime_no,
                        'salary_no':_post.salary_no,
                        'total_time':_post.total_time,
                        'fulltime':_post.fulltime,
                        'latetime':_post.latetime,
                        'attend_id':_post.attend_id,
                        'tel':_post.tel,
                        'work_position':_post.work_position

                    }
                    posts.append(post_data)

            if posts == []:
                Response = {
                    'status': 'Null',
                    'data': posts
                }
            else:
                Response = {
                    'status': 'Succeed',
                    'data': posts
                }
            #return Response
        except Exception as e:
            Response = {
                'status': 'Error',
                'msg': str(e)
            }
    else:
        try:
            all_posts = AttendanceEmpTodayView .objects.all()
            posts = []

            for _post in all_posts:  # 按照api格式塞進去
                punch_in=None if _post.punch_in==None else _post.punch_in.strftime("%Y-%m-%d %H:%M:%S")#三元運算子
                punch_out=None if _post.punch_out==None else _post.punch_out.strftime("%Y-%m-%d %H:%M:%S")
                if _post.group_no!=0 and _post.group_no!="0" and _post.group_no!="0":
                    post_data = {  # 按照api格式塞進去
                        'attend_no':_post.attend_no,
                        'attend_date':_post.attend_date,
                        'comp_name':_post.comp_name,
                        'shift_no':_post.shift_no,
                        'emp_no': _post.emp_no,
                        'emp_name':_post.emp_name,
                        'group_no':_post.group_no,
                        'punch_in':punch_in,
                        'punch_out':punch_out,
                        'in_position':_post.in_position,
                        'out_position':_post.out_position,
                        'overtime_no':_post.overtime_no,
                        'salary_no':_post.salary_no,
                        #'total_time':_post.total_time,
                        #'fulltime':_post.fulltime,
                        #'latetime':_post.latetime,
                        #'attend_id':_post.attend_id,
                        #'tel':_post.tel,
                        'work_position':_post.work_position

                    }
                    posts.append(post_data)

            if posts == []:
                Response = {
                    'status': 'Null',
                    'data': posts
                }
            else:
                Response = {
                    'status': 'Succeed',
                    'data': posts
                }
            #return Response
        except Exception as e:
            Response = {
                'status': 'Error',
                'msg': str(e)
            }

    
    return Response
