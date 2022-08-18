from datetime import date, datetime, timedelta
from operator import index

import requests
import geocoder
# import time
import json
from urllib.parse import urlparse, parse_qs, urlunparse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q, Sum
from django.templatetags.static import static
from django.views.decorators.http import require_http_methods, require_GET

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, PostbackEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate, \
    MessageTemplateAction, PostbackTemplateAction, URITemplateAction, FlexSendMessage, LocationSendMessage

from .models import ZzEmpTable, ZzAttendanceTable, ZzWorkOvertime, overtime_check_view, shifts_attendance_view, \
    CompanyTable, ShiftsTable, second_EmpTable, second_WorkOvertime,ShiftsTableNotF,shifts_attendance_view_line

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

geocoder_key='AnUFtLE-m30hzuhdc6uwnK1MLGx6_f2wL2iJlr2B_0CXoVnWiNI_9OEPB2L2d9fK'
# 捷利合
notify_token = 'h0A5uvDDbTf9ke3xnhxXwRXNVooe2hKLI6mUmygZKCR'
overtime_app_token = '3uiNSZxhWhYOak6H6T1QZdPH613XAW9rOOdZV5gMQbC'
overtime_check_token = 'B6cwz9X0jiOa8ggzwpjGyZ5x2RFOGfA3qyOIO53OQyz'
overtime_check_url="https://liff.line.me/1656458606-0EBQ8zGO"
get_location_url="https://liff.line.me/1656458606-r4Ve8oJM"
change_shift_time_url="https://liff.line.me/1656458606-3ywQOjlM"
myurl = 'https://cgpt-hrcs-linebot.azurewebsites.net'


def overtime_app_push(params_message):
    headers = {
        "Authorization": "Bearer " + overtime_app_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": params_message}

    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  # 200


def overtime_check_push(params_message):
    headers = {
        "Authorization": "Bearer " + overtime_check_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": params_message}

    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  # 200


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        message = []
        # 在這裡將body寫入機器人回傳的訊息中，可以更容易看出你收到的webhook長怎樣#
        message.append(TextSendMessage(text=str(body)))
        try:
            events = parser.parse(str(body), signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print(event.message.type)
                line_id = event.source.user_id
                hasuser_id = ZzEmpTable.objects.filter(
                    line_id=line_id).count()

                if event.message.type == 'text':
                    get_tel = ZzEmpTable.objects.filter(
                        tel=event.message.text).count()
                    has_tel = ZzEmpTable.objects.filter(
                        Q(tel=event.message.text, line_id__gt='') | Q(tel=event.message.text,
                                                                      line_id__isnull=True)).count()
                    if hasuser_id == 0 and get_tel == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                             TextSendMessage(text='請輸入登記的手機號碼')
                            # lineuid()
                        )
                    elif hasuser_id == 0 and get_tel > 0 and has_tel == 0:
                        ZzEmpTable.objects.filter(
                            tel=event.message.text).update(line_id=event.source.user_id)
                        user_name = ZzEmpTable.objects.get(
                            tel=event.message.text, line_id=event.source.user_id)
                        user_name = user_name.emp_no

                        backtext = '檢測到員工中有【' + event.message.text + '】手機號碼，已將您的LINE綁定員工編號【' + user_name + '】，可以開始使用打卡鐘功能了'
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(backtext)
                        )
                    elif hasuser_id == 0 and get_tel > 0 and has_tel > 0:
                        user_name = ZzEmpTable.objects.get(
                            tel=event.message.text)
                        user_name = user_name.emp_no
                        backtext = '檢測到員工中有【' + event.message.text + '】手機號碼，但此號碼已被綁定員工編號【' + user_name + '】，請洽公司詢問是否為誤綁'
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(backtext)
                        )
                    else:
                        # 先從line_id獲取員工資料emp.emp_no獲取員工編號
                        emp = ZzEmpTable.objects.filter(
                            line_id=line_id)[:1].get()
                        company = CompanyTable.objects.filter(  # 確認是登記在資料表內的公司
                            comp_no=emp.comp_no)
                        if not company:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='員工公司編屬有誤')
                            )
                            break
                        maincompany = company[0].main  # 判斷是否為此資料庫主公司員工
                        # nowtime取傳訊息時間； nowtime = datetime.now()-timedelta(seconds=5)取現在時間
                        nowtime = datetime.fromtimestamp(
                            event.timestamp / 1000)
                        nowtimestamp = event.timestamp
                        if event.message.text == 'help':
                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                                event.reply_token,
                                allhelp()

                            )
                        # text-上班打卡
                        elif event.message.text == '上班打卡':
                            showtime = nowtime.strftime(
                                '%Y-%m-%d %H:%M:%S')
                            # 確認上班打過卡了嗎
                            has_attendance = ZzAttendanceTable.objects.filter(
                                emp_no=emp.emp_no, attend_date=nowtime.date())

                            if has_attendance:
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    TextSendMessage(
                                        text='你已打卡上班於\n【' + str(has_attendance[0].punch_in) + '】')
                                )

                            else:
                                if maincompany == 1:  # 不包else與非主公司一起共用TemplateSendMessage
                                    shifts = ShiftsTable.objects.filter(
                                        date=nowtime.date(), emp_no=emp.emp_no)

                                    if not shifts:  # 本公司正職無斑表額外加班需去其他間公司
                                        line_bot_api.reply_message(
                                            event.reply_token,
                                            TextSendMessage(text="今天沒有排班喔！"))
                                        break
                                    else:  # 有班表打卡時間限制
                                        punch_in_time = nowtime - datetime.combine(nowtime.date(),
                                                                                   shifts[0].punch_in.time())
                                        total_time = punch_in_time.total_seconds() // 60  # 避免15.xx會顯示現在離排班時間還差15分鐘的怪異，負數//無條件捨去 -3.2//1=-4
                                        # 幾分鐘(15)以內才可以打上班卡(如果用正數判斷total_time要用/60)
                                        if total_time < -15:
                                            line_bot_api.reply_message(
                                                event.reply_token,
                                                TextSendMessage(
                                                    text="上班前15分鐘才能打卡，現在離排班時間還差" + str(int(abs(total_time))) + '分鐘'))
                                            break
                                tourl = '?punch=' + str(nowtimestamp) + '&emp_no=' + emp.emp_no + '&type=punchin'
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    TemplateSendMessage(
                                        alt_text='上班打卡：若要確認並傳送打卡地點',
                                        template=ButtonsTemplate(
                                            title=event.message.text,
                                            text='【' + emp.emp_name + '】' + event.message.text + '於\n' + str(
                                                showtime) + '\n(時效2分鐘)',
                                            actions=[
                                                URITemplateAction(
                                                    label='確認並傳送打卡地點',
                                                    uri=get_location_url + tourl
                                                ),
                                            ]
                                        )
                                    )
                                )
                        # text-下班打卡
                        elif event.message.text == '下班打卡':
                            # 確認上班打過卡了嗎
                            has_attendance = ZzAttendanceTable.objects.filter(
                                emp_no=emp.emp_no, attend_date=nowtime.date(), punch_in__isnull=False)  # 上班時間有值
                            has_attendance_out = ZzAttendanceTable.objects.filter(
                                emp_no=emp.emp_no, attend_date=nowtime.date(), punch_in__isnull=False,
                                punch_out__isnull=False)  # 上下班時間皆有值
                            overtime_hours = nowtime - has_attendance[0].punch_in
                            total_min = overtime_hours.seconds // 60  # 最小單位分鐘，捨小數
                            enoughtime = ''
                            if total_min < 540:
                                enoughtime = '上班總時數未達9小時(含休息時數)\n'
                            if has_attendance and not has_attendance_out:
                                # 儲存下班打卡時間
                                showtime = nowtime.strftime(
                                    '%Y-%m-%d %H:%M:%S')
                                tourl = '?punch=' + str(nowtimestamp) + '&emp_no=' + emp.emp_no + '&type=punchout'
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    TemplateSendMessage(
                                        alt_text='下班打卡：若要確認並傳送打卡地點',
                                        template=ButtonsTemplate(
                                            title=event.message.text,
                                            text=('%s【%s】%s於\n%s\n(時效2分鐘)' % (
                                            enoughtime, emp.emp_name, event.message.text, str(showtime))),
                                            actions=[
                                                URITemplateAction(
                                                    label='確認並傳送打卡地點',
                                                    uri=get_location_url + tourl
                                                ),
                                            ]
                                        )
                                    )
                                )

                            elif has_attendance and has_attendance_out:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(
                                        text='你已打卡下班於\n【' + str(has_attendance_out[0].punch_out) + '】\n請勿重複打卡')
                                )
                            else:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(
                                        text='今日並未上班(上班卡未打)')
                                )
                        # text-加班申請
                        elif event.message.text == '加班申請':

                            # 承攬制員工無此功能
                            if maincompany == 1:

                                # 確認上班打過卡了嗎(平日模式)
                                has_attendance = ZzAttendanceTable.objects.filter(
                                    emp_no=emp.emp_no, attend_date=nowtime.date(), punch_in__isnull=False)  # 上班時間有值
                                has_overtime_no = has_attendance.exclude(
                                    Q(overtime_no__exact='') | Q(overtime_no__isnull=True))  # 如果加班單號有值

                                if not has_attendance:
                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(
                                            text='上班卡未打，無法申請加班')
                                    )
                                elif has_attendance and has_overtime_no:

                                    overtime_table = ZzWorkOvertime.objects.filter(
                                        overtime_no__exact=has_overtime_no[0].overtime_no)
                                    overtimecheck = ''
                                    if overtime_table[0].overtime_check == 1:
                                        overtimecheck = '已通過核准'
                                    else:
                                        overtimecheck = '尚未核准'

                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(
                                            text='加班編號為' + has_overtime_no[0].overtime_no + overtimecheck)
                                    )
                                elif has_attendance and not has_overtime_no:

                                    attend_no = has_attendance[0].attend_no
                                    overtime_no = 'OT' + emp.emp_no + nowtime.strftime(
                                        '%Y%m%d')  # 編加班編號[OT+員編+年月日]
                                    # 編overtime_pay_no碼(暫以：[OTSN員編+年月]編排)
                                    overtime_pay_no = 'OTSN' + emp.emp_no + nowtime.strftime('%Y%m')
                                    overtime_table = ZzWorkOvertime.objects.filter(
                                        overtime_no__exact=overtime_no)
                                    if not overtime_table:
                                        ZzWorkOvertime.objects.create(
                                            overtime_no=overtime_no, attend_no=attend_no, overtime_date=nowtime.date(),
                                            overtime_pay_no=overtime_pay_no, emp_no=emp.emp_no)
                                        has_attendance.update(
                                            overtime_no=overtime_no)
                                        overtime_app_push_text = (
                                                '%s【%s】申請加班' % (emp.group_no.group_name, emp.emp_name))
                                        overtime_app_push(overtime_app_push_text)
                                        line_bot_api.reply_message(
                                            event.reply_token,
                                            TextSendMessage(
                                                text='加班申請，您的加班編號為' + overtime_no + '請等待核可'))
                                else:
                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(
                                            text='加班申請例外狀況'))
                            else:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(
                                        text='承攬制員工無此功能'))

                        # text-加班審核
                        elif event.message.text == '加班審核':

                            # 承攬制員工無此功能
                            if maincompany == 1:
                                if emp.group_leader == 1:
                                    tourl = '?emp_no=' + emp.emp_no
                                    contenttext = FlexSendMessage(
                                        alt_text=('%s-加班審核' % (emp.group_no.group_name)),
                                        # 本機版
                                        # contents={
                                        #     "type": "bubble",
                                        #     "size": "kilo",
                                        #     "body": {
                                        #         "type": "box",
                                        #         "layout": "vertical",
                                        #         "contents": [
                                        #             {
                                        #                 "type": "button",
                                        #                 "action": {
                                        #                     "type": "uri",
                                        #                     "label": str('%s-加班審核' % (emp.group_no.group_name)),
                                        #                     "uri": overtime_check_url + tourl
                                        #                 },
                                        #                 "height": "sm",
                                        #                 "style": "secondary",
                                        #                 "color": "#fbce98"
                                        #             },
                                        #             {
                                        #                 "type": "button",
                                        #                 "action": {
                                        #                     "type": "uri",
                                        #                     "label": str('%s-當日班表修改' % (emp.group_no.group_name)),
                                        #                     "uri": change_shift_time_url + tourl
                                        #                 },
                                        #                 "height": "sm",
                                        #                 "style": "secondary",
                                        #                 "color": "#fbce98"
                                        #             }
                                        #         ],
                                        #         "spacing": "sm"
                                        #     }
                                        # })
                                        # 捷利合版
                                        contents = {
                                            "type": "bubble",
                                            "size": "kilo",
                                            "body": {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {"type": "box",
                                                     "layout": "vertical",
                                                     "contents": [
                                                         {
                                                             "type": "button",
                                                             "action": {
                                                                 "type": "uri",
                                                                 "label": str('%s-加班審核' % (emp.group_no.group_name)),
                                                                  "uri": overtime_check_url + tourl
                                                             },
                                                             "height": "sm",
                                                             "color": "#32291E"
                                                         }],
                                                     "borderColor": "#ff8e58",
                                                     "borderWidth": "2px",
                                                     "cornerRadius": "10px"
                                                     },
                                                    {"type": "box",
                                                     "layout": "vertical",
                                                     "contents": [
                                                         {
                                                             "type": "button",
                                                             "action": {
                                                                 "type": "uri",
                                                                 "label": str('%s-當日班表修改' % (emp.group_no.group_name)),
                                                                  "uri": change_shift_time_url + tourl
                                                             },
                                                             "height": "sm",
                                                             "color": "#32291E"
                                                         }
                                                     ],
                                                     "borderColor": "#ff8e58",
                                                     "borderWidth": "2px",
                                                     "cornerRadius": "10px"}

                                                ],
                                                "spacing": "sm"
                                            }
                                    })

                                else:
                                    contenttext = TextSendMessage(
                                        text=('你不是 [%s] 組長沒有審核權限。' % (emp.group_no.group_name)))
                                    print(contenttext)
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    contenttext
                                )
                            else:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(
                                        text='承攬制員工無此功能'))
                        # text-加班打卡
                        elif event.message.text == '加班打卡':

                            has_attendance_out = ZzAttendanceTable.objects.filter(
                                emp_no=emp.emp_no, attend_date=nowtime.date(), punch_in__isnull=False,
                                punch_out__isnull=False)  # 如果上下班時間皆有值
                            has_overtime_no = has_attendance_out.exclude(
                                Q(overtime_no__exact='') | Q(overtime_no__isnull=True))  # 如果加班單號有值
                            if not has_attendance_out:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(
                                        text='下班卡未打，無法進行加班打卡')
                                )
                            elif has_attendance_out and not has_overtime_no:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(
                                        text='您尚未申請加班')
                                )
                            elif has_attendance_out and has_overtime_no:
                                overtime_table = ZzWorkOvertime.objects.filter(
                                    overtime_no__exact=has_overtime_no[0].overtime_no,
                                    punch_in__isnull=True)  # 確認有此加班TABLE也未打過加班上班卡
                                overtime_table_out = ZzWorkOvertime.objects.filter(
                                    overtime_no__exact=has_overtime_no[0].overtime_no,
                                    punch_out__isnull=True)  # 未打過加班下班

                                if overtime_table and overtime_table_out:
                                    showtime = nowtime.strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年',m='月',d='日')
                                    overtimecheck = ''

                                    overtimecheck = '\n\U00002705確認加班編號' + has_overtime_no[0].overtime_no + '申請已核可'

                                    #punch_in_time = nowtime - datetime.combine(nowtime.date(),
                                    #                                           overtime_table[0].starttime)
                                    #total_time = punch_in_time.total_seconds() // 60  # 避免15.xx會顯示現在離排班時間還差15分鐘的怪異，負數//無條件捨去 -3.2//1=-4
                                    # 幾分鐘(15)以內才可以打上班卡(如果用正數判斷total_time要用/60)
                                    # print(punch_in_time,overtime_table[0].starttime,total_time)
                                    # if total_time < -15:
                                    #     line_bot_api.reply_message(
                                    #         event.reply_token,
                                    #         TextSendMessage(
                                    #             text="加班上班前15分鐘才能打卡，現在離加班時間還差" + str(int(abs(total_time))) + '分鐘'))
                                    #     break

                                    # if overtime_table[0].overtime_check == 1:
                                    # overtimecheck = '\n\U00002705確認加班編號' + has_overtime_no[0].overtime_no + '申請已核可\n核准加班時間為'+('[%s-%s]'% (overtime_table[0].starttime,overtime_table[0].endtime))
                                    # else:
                                        # overtimecheck = '\n\U0001F631加班申請編號' + has_overtime_no[
                                        #     0].overtime_no + '尚未核准，請聯絡組長進行審核。'
                                    overtime_table.update(punch_in=nowtime)
                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(
                                            text='【' + emp.emp_name + '】' + '\n於' + str(
                                                showtime) + '\n加班上班打卡送出' + overtimecheck)
                                    )
                                elif not overtime_table and overtime_table_out:
                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(
                                            text='【' + emp.emp_name + '】' + '\n已於' + str(
                                                overtime_table_out[0].punch_in) + '\n加班上班打卡，請勿重複打卡')
                                    )
                                elif not overtime_table and not overtime_table_out:
                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(
                                            text='【' + emp.emp_name + '】' + '\n已於' + str(
                                                overtime_table_out[0].punch_in) + '至' + str(
                                                overtime_table_out[0].punch_out) + '\n加班結束，請勿重複打卡')
                                    )

                                else:

                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(
                                            text='加班打卡例外狀況')
                                    )
                        # text-加班結束
                        elif event.message.text == '加班結束':
                            overtime_no = 'OT' + emp.emp_no + nowtime.strftime(
                                '%Y%m%d')  # 編加班編號[OT+員編+年月日]
                            overtime_table = ZzWorkOvertime.objects.filter(
                                overtime_no__exact=overtime_no, )  # 確認有此加班TABLE
                            overtime_table_in = overtime_table.filter(
                                punch_in__isnull=False)  # 已經打過加班上班卡
                            overtime_table_out = overtime_table.filter(
                                punch_out__isnull=True)  # 未打過加班下班
                            showtime = nowtime.strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年',m='月',d='日')
                            # a = datetime(1986, 10, 4, 8, 00, 00)
                            # b = has_attendance[0].punch_in
                            # c=((b-a).seconds)/60
                            messagetext = '例外狀況'
                            monthhours_text = ''
                            if overtime_table:

                                monthhours = ZzWorkOvertime.objects.filter(emp_no=emp.emp_no,
                                                                           overtime_date__month=overtime_table[
                                                                               0].overtime_date.month,
                                                                           overtime_date__year=overtime_table[
                                                                               0].overtime_date.year).aggregate(
                                    mounth_hours=Sum('overtime_hours'))
                                print(monthhours)
                                if overtime_table_in and not overtime_table_out:

                                    messagetext = emp.emp_no + '\n已於' + str(overtime_table_in[0].punch_in) + '至' + str(
                                        overtime_table_in[0].punch_out) + '\n加班結束，請勿重複打卡'
                                elif overtime_table_in and overtime_table_out:
                                    punch_in = overtime_table_in[0].punch_in
                                    # 加班下班時間拉寬後15分鐘
                                    endtime_add15=datetime.combine(nowtime.date(), overtime_table_in[0].endtime) + timedelta(
                                        minutes=15)
                                    if nowtime>endtime_add15:
                                        print(endtime_add15)
                                        nowtime=endtime_add15
                                    overtime_hours = nowtime - overtime_table_out[0].punch_in
                                    total_min = overtime_hours.seconds // 60  # 最小單位分鐘，捨小數
                                    totaltimetext = ''
                                    if total_min > 240:
                                        totaltimetext = '\n\U0001F628超過平日加班4小時上限，僅計算4小時'
                                        # if not overtime_to_other_db(emp.emp_no, emp.line_id, nowtime, total_min,
                                        #                             overtime_table_out[0].overtime_check):
                                        #     line_bot_api.reply_message(  # 回復傳入的訊息文字
                                        #         event.reply_token,
                                        #         TextSendMessage(
                                        #             text='你沒有在加班承攬公司打卡系統綁定帳號，請先去綁定')
                                        #     )
                                        #     break
                                        # overtime_table_out.update(
                                        #     punch_out=(nowtime - timedelta(minutes=(total_min - 240))),
                                        #     overtime_hours=240)
                                        overtime_table_out.update(
                                            punch_out=nowtime,
                                            overtime_hours=240)
                                    else:
                                        overtime_table_out.update(
                                            punch_out=nowtime, overtime_hours=total_min)

                                    if monthhours['mounth_hours'] + total_min >= 2280:  # 月上限46小時-8小時
                                        monthhours_text = '\n\U0001F4A5當月可加班時數已不足8小時'

                                    messagetext = ('【%s】\n加班下班於%s\n今日加班開始於%s\n總計%s時%s分鐘' % (
                                    emp.emp_name, str(nowtime),str(punch_in), str(total_min // 60),
                                    str(total_min % 60))) + totaltimetext + monthhours_text

                                elif not overtime_table_in:
                                    messagetext = '今日未加班(並未打過加班上班)'
                            else:
                                overtime_no = 'OT' + emp.emp_no + (nowtime - timedelta(days=1)).strftime(
                                    '%Y%m%d')  # 編加班編號[OT+員編+年月日]
                                overtime_table = ZzWorkOvertime.objects.filter(
                                    overtime_no__exact=overtime_no, overtime_date=nowtime - timedelta(days=1),
                                    punch_out__isnull=True)  # 是否跨日加班(昨天有資料且未下班)
                                if overtime_table:

                                    # 加班下班時間
                                    endtime_add15 = datetime.combine(nowtime.date(),overtime_table_in[0].endtime) + timedelta(
                                        minutes=15)
                                    if nowtime > endtime_add15:
                                        nowtime = endtime_add15
                                    overtime_hours = nowtime - overtime_table[0].punch_in
                                    total_min = overtime_hours.seconds // 60  # 最小單位分鐘，捨小數
                                    totaltimetext = ''
                                    if total_min > 240:
                                        totaltimetext = '\n\U0001F628超過平日加班4小時上限，僅計算4小時'
                                        # if not overtime_to_other_db(emp.emp_no, emp.line_id, nowtime, total_min,
                                        #                             overtime_table[0].overtime_check):
                                        #     line_bot_api.reply_message(  # 回復傳入的訊息文字
                                        #         event.reply_token,
                                        #         TextSendMessage(
                                        #             text='你沒有在加班承攬公司打卡系統綁定帳號，請先去綁定')
                                        #     )
                                        #     break
                                        # overtime_table.update(
                                        #     punch_out=(nowtime - timedelta(minutes=(total_min - 240))),
                                        #     overtime_hours=240)
                                        overtime_table.update(
                                            punch_out=nowtime,
                                            overtime_hours=240)
                                    else:
                                        overtime_table.update(
                                            punch_out=nowtime, overtime_hours=total_min)
                                    punch_in = str(overtime_table[0].punch_in)
                                    messagetext = ('【%s】\n加班下班於%s(跨日)\n此次加班開始於%s\n總計%s時%s分鐘' % (
                                    emp.emp_name, showtime, punch_in, str(total_min // 60),
                                    str(total_min % 60))) + totaltimetext + monthhours_text

                                else:
                                    messagetext = '今日未加班'

                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                                event.reply_token,
                                TextSendMessage(
                                    text=messagetext)
                            )
                        # text-加班結束
                        elif event.message.text == '班表查詢':
                            messagetext = 'test'
                            if maincompany == 1:
                                sevendays = nowtime.date() + timedelta(days=7)
                                print(sevendays)
                                sevenshifts = ShiftsTable.objects.filter(emp_no=emp.emp_no,
                                                                         date__range=[nowtime, sevendays])
                                print(sevenshifts)
                                messagetext = calendar(sevenshifts, nowtime.date(), sevendays)
                            else:
                                messagetext = TextSendMessage(text='承攬制員工無排定班表')
                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                                event.reply_token,
                                messagetext

                            )

                        # text-薪資查詢
                        elif event.message.text == '薪資查詢':
                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                                event.reply_token,
                                TextSendMessage(
                                    text='此功能尚未開發')

                            )
                        # text-取得地址
                        elif event.message.text == 'getalladdr':
                            Attendance_withoutaddr=ZzAttendanceTable.objects.filter(Q(in_addr__isnull=True)|Q(in_addr='')|Q(out_addr__isnull=True)|Q(out_addr=''))
                            for withoutaddr in Attendance_withoutaddr:

                                print(withoutaddr.in_position)
                                print(withoutaddr.out_position)
                                out_addr=None
                                in_addr=None

                                if withoutaddr.out_position:
                                    location = withoutaddr.out_position.split(',')
                                    out_addr = geocoder.bing(location, key=geocoder_key, method='reverse').json[
                                        'address']

                                if withoutaddr.in_position:
                                    location = withoutaddr.in_position.split(',')
                                    in_addr = geocoder.bing(location, key=geocoder_key, method='reverse').json[
                                        'address']
                                # withoutaddr.filter(attend_no=withoutaddr.attend_no).update(in_addr=in_addr,out_addr=out_addr)
                                withoutaddr.in_addr=in_addr
                                withoutaddr.out_addr=out_addr
                                withoutaddr.save()

                                # location = urlquery['location'][0].split(',')
                                # addr = geocoder.bing(location, key=geocoder_key, method='reverse').json['address']
                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(
                                text='getalladdr')

                        )

                        else:  # 其他奇奇怪怪的字輸入
                            test2 = ZzWorkOvertime.objects.filter(overtime_date__month='7',
                                                                  overtime_date__year='2021').aggregate(
                                mounth_hours=Sum('overtime_hours'))
                            print(test2['mounth_hours'])
                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                                event.reply_token,
                                default_jsoncontent()
                                # TextSendMessage(str(test2))
                                # TemplateSendMessage(
                                #     alt_text='Buttons template',
                                #     template=ButtonsTemplate(
                                #         title=event.message.text,
                                #         text='若請求權限請按接受',
                                #         actions=[
                                #             URITemplateAction(
                                #                 label='傳送打卡地點',
                                #                 uri='https://liff.line.me/1656140947-gvkw2yjJ?HH=123&FF=345'
                                #                 # uri='https://liff.line.me/1654046335-DzXpM8mx?HH=123&FF=345'

                                #             ),
                                #         ]
                                #     )
                                # )
                            )
                # image訊息
                elif event.message.type == 'image':
                    if hasuser_id == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            # TextSendMessage(text='請輸入登記的手機號碼')
                            lineuid()
                        )
                    else:
                        messagetext = '無效訊息'
                        if event.message.content_provider.original_content_url:
                            # 先從line_id獲取員工資料emp.emp_no獲取員工編號
                            emp = ZzEmpTable.objects.filter(
                                line_id=line_id)[:1].get()
                            company = CompanyTable.objects.filter(  # 確認是登記在資料表內的公司
                                comp_no=emp.comp_no)
                            if not company:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text='員工公司編屬有誤')
                                )
                                break
                            maincompany = company[0].main
                            # nowtime取傳訊息時間； nowtime = datetime.now()-timedelta(seconds=5)取現在時間
                            imgdata = event.message.content_provider.original_content_url
                            urlquery = parse_qs(urlparse(imgdata).query)
                            imgfunc = urlquery['type'][0]
                            # image-上班卡
                            if imgfunc == 'punchin':  # 上班卡
                                if urlquery['emp_no'][0] == emp.emp_no:
                                    gettime = datetime.fromtimestamp(
                                        int(urlquery['punch'][0]) / 1000)
                                    #showtime = gettime.strftime('%Y年%m月%d日 %H:%M:%S')
                                    showtime = gettime.strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年',m='月',d='日')
                                    attend_no_count = 'ATT' + emp.emp_no + gettime.strftime('%Y%m%d')
                                    # +str(ZzAttendanceTable.objects.filter(attend_date=gettime.date()).count()+1)  # 編attend_no碼(暫以：[ATT+日期+該日期筆數]編排)
                                    # 編salary_no碼(暫以：[SN員編+年月]編排)
                                    salary_no = 'SN' + emp.emp_no + \
                                                gettime.strftime('%Y%m')
                                    has_attendance = ZzAttendanceTable.objects.filter(
                                        emp_no=emp.emp_no, punch_in=gettime.strftime('%Y-%m-%d %H:%M:%S'),
                                        attend_date=gettime.date(), salary_no=salary_no)  # 上班時間重複?不檢查地點

                                    if not has_attendance:
                                        if maincompany == 1:
                                            shifts = ShiftsTable.objects.filter(
                                                date=gettime.date(), emp_no=emp.emp_no)
                                            if shifts:
                                                # 算遲到15分(不算了，遲到一分鐘也記錄
                                                total_min_text = ''
                                                total_min = 0

                                                if gettime>shifts[0].punch_in:
                                                    overtime_hours = gettime - shifts[0].punch_in
                                                    total_min = overtime_hours.seconds // 60  # 最小單位分鐘，捨小數
                                                    total_min_text = '\n遲到：' + str(total_min) + '分鐘'

                                                # # if total_min<15:
                                                #     total_min=0
                                                #     total_min_text=''

                                                #根據經緯度取得地址(英文)
                                                location=urlquery['location'][0].split(',')
                                                addr = geocoder.bing(location, key=geocoder_key,method='reverse')

                                                ZzAttendanceTable.objects.create(
                                                    emp_no=emp.emp_no, punch_in=gettime, attend_date=gettime.date(),
                                                    attend_no=attend_no_count, salary_no=salary_no,
                                                    shift_no=shifts[0].shift_no, in_position=urlquery['location'][0],in_addr=addr.json['address'],
                                                    latetime=total_min)
                                                shifts.update(
                                                    attend_no=attend_no_count)
                                                # messagetext = '【' + emp.emp_name + '】上班打卡於\n' + str(
                                                #     showtime) + total_min_text
                                                location_str_list = urlquery['location'][0].split(',')
                                                messagetext = LocationSendMessage(
                                                    title=('【%s】上班打卡' % (emp.emp_name)),
                                                    address=str(showtime)+ total_min_text,
                                                    latitude=location_str_list[0],
                                                    longitude=location_str_list[1]
                                                )
                                        else:
                                            # 根據經緯度取得地址(英文)
                                            location = urlquery['location'][0].split(',')
                                            addr = geocoder.bing(location, key=geocoder_key, method='reverse')
                                            ZzAttendanceTable.objects.create(
                                                emp_no=emp.emp_no, punch_in=gettime, attend_date=gettime.date(),
                                                attend_no=attend_no_count, salary_no=salary_no,in_addr=addr,
                                                in_position=urlquery['location'][0])
                                            messagetext = TextSendMessage('【' + emp.emp_name + '】上班打卡於\n' + str(showtime))
                                    else:
                                        messagetext = TextSendMessage('您已上班打卡於\n' + str(showtime))
                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        messagetext
                                    )
                                    break
                            # image-下班卡
                            if imgfunc == 'punchout':  # 下班卡
                                if urlquery['emp_no'][0] == emp.emp_no:
                                    gettime = datetime.fromtimestamp(
                                        int(urlquery['punch'][0]) / 1000)
                                    showtime = gettime.strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年',m='月',d='日')
                                    has_attendance = ZzAttendanceTable.objects.filter(
                                        emp_no=emp.emp_no, attend_date=gettime.date(), punch_in__isnull=False,
                                        punch_out__isnull=True)  # 有上班紀錄且下班時間是null
                                    has_attendance_same = has_attendance.filter(
                                        punch_out=gettime.strftime('%Y-%m-%d %H:%M:%S'))  # 下班時間重複?

                                    if has_attendance and not has_attendance_same:
                                        # 算遲到15分
                                        overtime_hours = gettime - has_attendance[0].punch_in
                                        total_min = overtime_hours.seconds // 60  # 最小單位分鐘，捨小數
                                        fulltime = 1
                                        if total_min < 540:  # 未滿9小時
                                            fulltime = 0
                                        # 根據經緯度取得地址(英文)
                                        location = urlquery['location'][0].split(',')
                                        addr = geocoder.bing(location, key=geocoder_key, method='reverse')

                                        has_attendance.update(
                                            punch_out=gettime, out_position=urlquery['location'][0], fulltime=fulltime,out_addr=addr.json['address'],
                                            total_time=total_min)
                                        # messagetext = '【' + emp.emp_name + \
                                        #               '】下班打卡於\n' + str(showtime)+'\n位置：'+urlquery['location'][0]
                                        location_str_list=urlquery['location'][0].split(',')
                                        messagetext=LocationSendMessage(
                                            title=('【%s】下班打卡' % (emp.emp_name)),
                                            address= str(showtime),
                                            latitude=location_str_list[0],
                                            longitude=location_str_list[1]
                                        )

                                    elif has_attendance and has_attendance_same:
                                        messagetext=TextSendMessage ('您已下班打卡於\n' + str(showtime))
                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        messagetext
                                    )
                                    break
                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                                event.reply_token,
                                default_jsoncontent()
                            )

                        # message.append(TextSendMessage(text='圖片訊息'))
                        # line_bot_api.reply_message(event.reply_token, message)
                elif event.message.type == 'location':
                    if hasuser_id == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入登記的手機號碼')
                            # lineuid()
                        #     測試用才抓列出給人選
                        )
                    else:
                        message.append(TextSendMessage(text='位置訊息'))
                        line_bot_api.reply_message(event.reply_token, message)
                else:
                    print(event.message.type)
            elif isinstance(event, PostbackEvent):
                print('PostbackEvent')
                print(event.postback.data)
                getpostdata = event.postback.data
                messagejson = default_jsoncontent()
                # punch_help()

                if getpostdata == 'punch_help':
                    messagejson = punch_help()
                elif getpostdata == 'lineAccessRights' or getpostdata == 'LocationAuthorization':
                    messagejson = help_punch_alert()
                elif getpostdata == 'help':
                    messagejson = allhelp()
                elif getpostdata == 'overtime_check_help':
                    messagejson = overtime_check_help()
                elif getpostdata == 'overtime_app_help':
                    messagejson = overtime_app_help()
                    # messagejson = lineuid()
                elif getpostdata == 'change_shift_time_help':
                    messagejson = change_shift_time_help()
                elif getpostdata == 'line_help':
                    line_id = event.source.user_id
                    hasuser_id = ZzEmpTable.objects.filter(
                        line_id=line_id)
                    if hasuser_id:
                        messagejson = TextSendMessage('你已經綁定帳號了。')
                    else:
                        messagejson = lineuid()

                line_bot_api.reply_message(
                    event.reply_token,
                    messagejson
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def punch_help():
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_stap1.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "1.按下打卡",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "上班打卡 或 下班打卡 步驟皆相同",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }, {
                                            "type": "text",
                                            "text": "若未排班，會返回[今天沒有排班]",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }, {
                                            "type": "text",
                                            "text": "若已打過卡，會回傳今天打卡的時間",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_stap2.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "2.點選【確認並傳送打卡地點】",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "按下按鈕才是確認打卡，紀錄的時間會是第1步驟時就傳送的時間(避免誤打卡，故你需要多按這次確認)",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "此按紐在2分鐘後會過期無法正確打卡",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xxs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_stap3.png') + '?v=2',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "3.等待位置傳送並打卡",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "將開啟一個一半的頁面，在時效內位置傳送成功即會自行關閉",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "手機定位請記得開啟",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xxs",
                                            "flex": 5
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "存取權限?",
                                        "data": "lineAccessRights"
                                    },
                                    "height": "sm",
                                    "margin": "none",
                                    "offsetTop": "5px"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "授權問題?",
                                        "data": "LocationAuthorization"
                                    },
                                    "margin": "none",
                                    "height": "sm"
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px",
                    "paddingBottom": "0px"
                }
            }
        ]
    }
    message = FlexSendMessage(alt_text='打卡教學', contents=content)
    return message


def help_punch_alert():
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "kilo",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_alert1.png') + '?v=2',
                    "size": "full",
                    "aspectRatio": "320:213",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "LINE存取權限",
                            "weight": "bold",
                            "size": "md",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "第一次使用打卡功能會跳出程式授權請求存取權限，請按許可",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "kilo",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_alert2.png') + '?v=2',
                    "size": "full",
                    "aspectRatio": "320:213",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "打卡位置資訊授權",
                            "weight": "bold",
                            "size": "md",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "打卡網頁會搜尋您所在的位置，並會跳出請求授權，請按確定",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            }
        ]
    }
    message = FlexSendMessage(alt_text='驗證及授權幫助', contents=content)
    return message


def allhelp():
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "kilo",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "幫助",
                            "weight": "bold",
                            "size": "md",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "你想問什麼問題?",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "打卡教學上下班通用",
                                                "data": "punch_help"
                                            },
                                            "height": "sm"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "加班申請與審核狀態",
                                                "data": "overtime_app_help"
                                            },
                                            "height": "sm",
                                            "style": "primary",
                                            "color": "#226699"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "程式授權與存取",
                                                "data": "lineAccessRights"
                                            },
                                            "height": "sm"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "加班審核教學",
                                                "data": "overtime_check_help"
                                            },
                                            "height": "sm",
                                            "style": "primary",
                                            "color": "#226699"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "line綁定問題",
                                                "data": "line_help"
                                            },
                                            "height": "sm"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "修改組員當日班表教學",
                                                "data": "change_shift_time_help"
                                            },
                                            "height": "sm",
                                            "style": "primary",
                                            "color": "#226699"
                                        },
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px",
                    "paddingBottom": "0px"
                }
            }
        ]
    }
    message = FlexSendMessage(alt_text='需要幫助嗎?', contents=content)
    return message


def default_jsoncontent():  # 我不懂你的意思
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "micro",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "我不懂你的意思",
                            "weight": "bold",
                            "size": "md",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "你需不需要",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "尋求幫助",
                                                "data": "help"
                                            },
                                            "height": "sm"
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px",
                    "paddingBottom": "0px"
                }
            }
        ]
    }
    message = FlexSendMessage(alt_text='需要幫助嗎?', contents=content)
    return message


def overtime_check_help():  # 加班審核
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/overtime_check1.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "1.按下加班審核",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "只有組長有審核該組權限",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xs",
                                            "flex": 5
                                        }, {
                                            "type": "text",
                                            "text": "承攬制員工無此功能",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/overtime_check2.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "2.點擊審核組別按鈕，開啟審核頁面",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "審核頁面開啟前系統會自動執行身份驗證",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }, {
                                            "type": "text",
                                            "text": "只有在手機上才可進行審核",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xs",
                                            "flex": 5
                                        }

                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/overtime_check3.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "3.選擇今日可加班人選(可複選)，確認送出",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "組員若有自行申請加班會標上待審中的紅標籤、已審核通過的也會有綠標籤(且無法再次點選)",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "組員未申請加班，組長也可直接幫其開通當日加班",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "僅會列出當日有出勤的組員",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/overtime_check4.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "4.開通加班成功後，審核用群組收到通知",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "審核送出後，系統會自動發訊息給群組，訊息內容會區分員工是自行申請加班、或組長直接開通",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            }

        ]
    }

    message = FlexSendMessage(alt_text='加班審核?', contents=content)
    return message


def overtime_app_help():  # 加班申請
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/overtime_app1.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "1.按下加班申請",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "請在今日已打卡上班後才進行加班申請",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xs",
                                            "flex": 5
                                        }, {
                                            "type": "text",
                                            "text": "若今日未上班點選此按鈕，將顯示 [上班卡未打，無法申請加班]",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }, {
                                            "type": "text",
                                            "text": "承攬制員工無此功能",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/overtime_app2.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "2.傳送訊息給審核通知用群組",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "申請送出同時，系統會自動發訊息給群組",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/overtime_app3.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "3.再次點選加班申請按鈕，可以知道該筆申請是否被核准",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "回傳今天提出的加班申請狀態，分為 [尚未核准]、[已通過核准]",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "(加班申請編號會在第一次按下時產生)",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xxs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            }

        ]
    }
    message = FlexSendMessage(alt_text='加班申請?', contents=content)
    return message


def change_shift_time_help():  # 加班審核
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/overtime_check1.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "1.按下加班審核",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "只有組長有審核該組權限",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "承攬制員工無此功能",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/change_shift_2.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "2.點擊[組別-當日班表修改]，開啟修改頁面",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "修改頁面開啟前系統會自動執行身份驗證",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "僅會列出當日有排班的組員",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "只有在手機上才可進行修改",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/change_shift_3.png') + '?v=1',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "3.選擇修改人選點擊展開，時間或備註修改完成後按[修改]",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "會顯示當前組員出勤狀態(值勤中、已下班、未上班)",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "可單獨修改備註或時間",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "若僅修改時間，系統會自動添加新舊時間備註",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            }
        ]
    }

    message = FlexSendMessage(alt_text='當日班表修改?', contents=content)
    return message


def calendar(sevenshifts, nowday, sevenday):
    calendar_days = []
    justline = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "flex": 3
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "filler"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "width": "2px",
                                "backgroundColor": "#B7B7B7"
                            },
                            {
                                "type": "filler"
                            }
                        ],
                        "flex": 1
                    }
                ],
                "width": "12px"
            },
            {
                "type": "text",
                "text": " ",
                "gravity": "center",
                "flex": 4
            }
        ],
        "spacing": "lg",
        "height": "15px"

    }

    i = 0
    while i <= 7:
        punchtext = '休'
        addday = nowday + timedelta(days=i)
        weekday_list = ['一', '二', '三', '四', '五', '六', '日']
        text_color = '#999999'
        circle_color = '#999999'
        weekday = addday.weekday()

        if sevenshifts:
            sevenshifts_addday = sevenshifts.filter(date=addday)
            if sevenshifts_addday:

                if addday == sevenshifts_addday[0].date:
                    punch_in = sevenshifts_addday[0].punch_in.strftime('%H:%M')
                    punch_out = sevenshifts_addday[0].punch_out.strftime('%H:%M')
                    punchtext = punch_in + ' - ' + punch_out
                    circle_color = '#6486E3'
                    text_color = '#000000'
        if i == 0:
            datetext = '今天'
            circle_color = '#EF454D'
            text_color = '#000000'
        else:
            datetext = ('%s (%s)' % (str(addday), weekday_list[weekday]))
        if i != 0:
            calendar_days.append(justline)

        bottonitem = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": punchtext,
                    "size": "sm",
                    "flex": 3,
                    "align": "end"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [],
                            "cornerRadius": "30px",
                            "height": "12px",
                            "width": "12px",
                            "borderColor": circle_color,
                            "borderWidth": "2px"
                        },
                        {
                            "type": "filler"
                        }
                    ],
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": datetext,
                    "color": text_color,
                    "gravity": "center",
                    "flex": 4,
                    "size": "sm"
                }
            ],
            "spacing": "lg"
        }

        calendar_days.append(bottonitem)

        i = i + 1

    content = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": myurl + static('img/Cc.png') + '?v=2',
                    "position": "absolute",
                    "offsetEnd": "15px",
                    "offsetBottom": "0px",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "自",
                            "color": "#ffffff66",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": str(nowday),
                            "color": "#ffffff",
                            "size": "lg",
                            "flex": 4,
                            "weight": "bold"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "到",
                            "color": "#ffffff66",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": str(sevenday),
                            "color": "#ffffff",
                            "size": "lg",
                            "flex": 4,
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "僅供參考",
                            "color": "#ffffff66",
                            "size": "xs"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "color": "#555555",
                            "size": "xl",
                            "text": "7日班表",
                            "weight": "bold",
                            "wrap": True,
                            "align": "center"
                        }
                    ],
                    "position": "absolute",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "width": "30px",
                    "offsetEnd": "5px",
                    "offsetBottom": "5px"
                }
            ],
            "height": "154px",
            "background": {
                "type": "linearGradient",
                "angle": "90deg",
                "startColor": "#5d3413",
                "endColor": "#FFFFFF",
                "centerPosition": "75%",
                "centerColor": "#FFFFFF"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": calendar_days,
            "paddingTop": "10px"
        }
        # footer之後新增表格
        # ,"footer": {
        #     "type": "box",
        #     "layout": "vertical",
        #     "contents": [
        #         {
        #             "type": "button",
        #             "action": {
        #                 "type": "uri",
        #                 "label": "看排班表格",
        #                 "uri": "http://linecorp.com/"
        #             },
        #             "height": "sm",
        #             "style": "link",
        #             "color": "#a48770",
        #             "margin": "none"
        #         }
        #     ],
        #     "paddingAll": "none"
        # }
    }
    message = FlexSendMessage(alt_text='7日排班', contents=content)
    return message


def lineuid():
    hasCanUseTel = ZzEmpTable.objects.filter(
        line_id__exact='').values('tel', 'emp_name')
    botton = [
        {
            "type": "text",
            "text": "開發測試環境有以下號碼供選擇▼",
            "wrap": True,
            "color": "#8c8c8c",
            "size": "xs",
            "flex": 5
        }

    ]
    if hasCanUseTel:
        maxchoose=5
        for idx, name in enumerate(hasCanUseTel):
            if maxchoose>0:
                bottonitem = {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": name['emp_name'] + ' / ' + name['tel'],
                        "text": name['tel']
                    },
                    "height": "sm"
                }
                botton.append(bottonitem)
                maxchoose-=1

    else:
        bottonitem = {
            "type": "text",
            "text": "Oops！沒有空的帳號了，請洽程式人員開設",
            "size": "md",
            "wrap": True,
            "margin": "xxl",
            "align": "center",
            "offsetBottom": "8px"
        }
        botton.append(bottonitem)
    content = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "首次使用需綁定帳號，請輸入登記的手機號碼",
                    "weight": "bold",
                    "size": "md",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": botton
                        }
                    ]
                }
            ],
            "spacing": "sm",
            "paddingAll": "13px",
            "paddingBottom": "0px"
        }
    }
    message = FlexSendMessage(alt_text='Line帳號綁定輔助', contents=content)
    return message


def overtime_to_other_db(emp_no, line_id, nowtime, total_min, overtime_check):
    second_emp = second_EmpTable.objects.filter(line_id=line_id)  # 另一張表該員工的員工編號
    if second_emp:

        second_emp_no = second_emp[0].emp_no
        overtime_no = 'OT' + second_emp_no + nowtime.strftime('%Y%m%d')  # 編加班編號[OT+員編+年月日]
        overtime_pay_no = 'OTSN' + second_emp_no + nowtime.strftime('%Y%m')
        punch_in_time = nowtime - timedelta(minutes=(total_min - 240))
        second_total_min = total_min - 240

        second_WorkOvertime.objects.create(emp_no=second_emp_no, overtime_no=overtime_no,
                                           overtime_date=punch_in_time.date(), punch_in=punch_in_time,
                                           punch_out=nowtime, overtime_hours=second_total_min,
                                           overtime_pay_no=overtime_pay_no, overtime_check=overtime_check)
        return True
    else:
        return False  # '你沒有在加班公司綁定帳號，請先綁定'

@require_GET
def get_location(request):
    return render(request, "get_location.html")

@require_GET
def overtime_check(request):
    if request.GET.get('emp_no'):
        emp_no = request.GET.get('emp_no')

        groupleader = ZzEmpTable.objects.filter(
            emp_no=emp_no, group_leader=1)
        if groupleader:
            groupleader = groupleader[0]
            groupleaderlineid = groupleader.line_id
            groupleader_empno = groupleader.emp_no

            # Attendance = ZzAttendanceTable.objects.raw(
            #     'SELECT * FROM zz_ATTENDANCE_TABLE where EMP_NO in(SELECT EMP_NO from EMP_TABLE where GROUP_NO=%s) and ATTEND_DATE >%s', [groupleader[0].group_no, '20210701'])

            nowdate = datetime.now()

            print(nowdate)
            emplist = ZzEmpTable.objects.filter(
                group_no=groupleader.group_no).values_list('emp_no', flat=True)
            print(groupleader.group_no)
            print(emplist)
            emplist = list(emplist)
            # 還沒加上過濾只要當天日期
            overtime_view = overtime_check_view.objects.filter(  # 還沒加nowdate
                attend_date=nowdate, emp_no__in=emplist).values('emp_no', 'overtime_no', 'overtime_check', 'tel',
                                                                'emp_name', 'attend_no')

            return render(request, "overtimecheck.html", {'emp': overtime_view, 'groupleaderlineid': groupleaderlineid,
                                                          'groupleader_empno': groupleader_empno})
        else:
            return render(request, "overtimecheck.html", {'groupleader_empno': '0'})
    else:
        return render(request, "overtimecheck.html")

@require_http_methods(["POST"])
def overtime_check_save(request):
    if request.POST:
        print(request.POST.getlist('attend_no'))
        emp_no = request.POST['groupleader']
        groupleader = ZzEmpTable.objects.filter(emp_no=emp_no, group_leader=1)
        if groupleader:
            groupleader = groupleader[0]
            groupleaderlineid = groupleader.line_id
            groupleader_empno = groupleader.emp_no

            nowdate = datetime.now()

            if request.POST.getlist('attend_no'):
                overtime_app_check_text = ('%s-%s' % (groupleader.group_no.group_no, groupleader.group_no.group_name))
                print(groupleader.group_no.group_name)
                starttime = request.POST['starttime']
                endtime = request.POST['endtime']
                print(starttime,endtime,type(endtime))
                for attend_no in request.POST.getlist('attend_no'):

                    print(attend_no)

                    overtime_check = overtime_check_view.objects.filter(attend_no=attend_no)


                    if overtime_check and overtime_check[0].overtime_no and overtime_check[0].overtime_check == 0:
                        overtime_check = overtime_check[0]
                        ZzWorkOvertime.objects.filter(attend_no=attend_no).update(overtime_check=1,starttime=starttime,endtime=endtime)
                        overtime_app_check_text += (
                                    '\n員編%s【%s】申請已核准' % (overtime_check.emp_no, overtime_check.emp_name))
                    else:
                        overtime_check = overtime_check[0]
                        overtime_no = 'OT' + overtime_check.emp_no + datetime.strftime(overtime_check.attend_date,
                                                                                       '%Y%m%d')
                        overtime_pay_no = 'OTSN' + overtime_check.emp_no + datetime.strftime(overtime_check.attend_date,
                                                                                             '%Y%m')

                        print(overtime_no)
                        print(overtime_pay_no)
                        ZzAttendanceTable.objects.filter(attend_no=attend_no).update(overtime_no=overtime_no)
                        ZzWorkOvertime.objects.create(overtime_no=overtime_no, attend_no=attend_no,
                                                      overtime_date=overtime_check.attend_date,
                                                      overtime_pay_no=overtime_pay_no, emp_no=overtime_check.emp_no,starttime=starttime,endtime=endtime,
                                                      overtime_check=1)
                        overtime_app_check_text += (
                                    '\n員編%s【%s】開通今日加班' % (overtime_check.emp_no, overtime_check.emp_name))

                overtime_check_push(overtime_app_check_text+'\n[時段為%s-%s]' % (starttime,endtime))

            emplist = ZzEmpTable.objects.filter(
                group_no=groupleader.group_no).values_list('emp_no', flat=True)
            emplist = list(emplist)
            overtime_view = overtime_check_view.objects.filter(  # 還沒加nowdate
                emp_no__in=emplist, attend_date=nowdate).values('emp_no', 'overtime_no', 'overtime_check', 'tel',
                                                                'emp_name', 'attend_no')
            return render(request, "overtimecheck.html", {'emp': overtime_view, 'groupleaderlineid': groupleaderlineid,
                                                          'groupleader_empno': groupleader_empno})
        else:
            return render(request, "overtimecheck.html")
    else:
        return render(request, "overtimecheck.html")

def change_shift_time(request):  
    if request.method == 'GET':
        #刪除
        if(request.GET.get('del')):
            ShiftsTable.objects.filter(shift_no=request.GET.get('del')).delete()

        if request.GET.get('emp_no'):
            emp_no = request.GET.get('emp_no')
            # print(emp_no)
            groupleader = ZzEmpTable.objects.filter(
                emp_no=emp_no, group_leader=1)
            if groupleader:
                groupleader = groupleader[0]
                groupleaderlineid = groupleader.line_id
                groupleader_empno = groupleader.emp_no

                # Attendance = ZzAttendanceTable.objects.raw(
                #     'SELECT * FROM zz_ATTENDANCE_TABLE where EMP_NO in(SELECT EMP_NO from EMP_TABLE where GROUP_NO=%s) and ATTEND_DATE >%s', [groupleader[0].group_no, '20210701'])
                if request.GET.get('date'):
                    nowdate = request.GET.get('date')
                else:
                    nowdate = datetime.now().strftime('%Y-%m-%d')

                # print(nowdate)
                emplist = ZzEmpTable.objects.filter(
                    Q(group_no=groupleader.group_no)& Q(working =1)).values_list('emp_no', flat=True)
                # print(groupleader.group_no)
                # print(emplist)
                emplist = list(emplist)

                all_posts = ShiftsTable.objects.filter(emp_no__in=emplist).values('emp_no','date')
               
                #不得連續上7天班
                for emp in emplist:
                    i=0
                    for post in all_posts:
                            if(emp == post["emp_no"]):
                                if((datetime.strptime(nowdate, '%Y-%m-%d')+ timedelta(days=-7)).date() <(post["date"]) <(datetime.strptime(nowdate, '%Y-%m-%d')).date()):
                                    i+=1

                    if(i>5):
                        emplist.pop(emplist.index(emp))


                # 還沒加上過濾只要當天日期
                shifts_view = shifts_attendance_view_line.objects.filter(
                Q(emp_no__in=emplist)).values('emp_no', 'emp_name', 'shift_no', 'text', 'punch_in','date',
                                                             'punch_out', 'att_punch_in', 'att_punch_out').order_by('date')


                shiftsList=[]
                for sh in shifts_view: 
                    if(sh["date"] != None):
                        sh["date"] =sh["date"].strftime('%Y-%m-%d')

                    if (sh["date"]== nowdate):                      
                        if(len(shiftsList)>0):
                            i=0
                            for shl in shiftsList:                             
                                if(shl["emp_no"] == sh["emp_no"]):
                                    i= i+1
     
                            if(i==0):                                                       
                                shiftsList.append(sh)     
                        else:
                            shiftsList.append(sh)   
                    # elif(sh["date"] == None):
                    #     shiftsList.append(sh)              
                    # else:
                for sh in shifts_view:     
                        i=0
                        for shl in shiftsList:
                            if(shl["emp_no"] == sh["emp_no"]):
                                i+=1

                        if(i==0):
                            sh["date"] =None
                            sh["shift_no"] =None
                            sh["punch_out"] =None
                            sh["punch_in"] =None
                            sh["text"] =None
                            sh["att_punch_in"] =None
                            sh["att_punch_out"] =None
                            shiftsList.append(sh)

  
                return render(request, "change_shift_time.html",
                              {'emp': shiftsList, 'groupleaderlineid': groupleaderlineid,
                               'groupleader_empno': groupleader_empno,'nowdate':nowdate,
                               'emplist': emplist})
            else:
                return render(request, "change_shift_time.html", {'groupleader_empno': '0'})
        else:
            return render(request, "change_shift_time.html")

    elif request.POST:
        emp_no = request.POST['groupleader']
       
        groupleader = ZzEmpTable.objects.filter(emp_no=emp_no, group_leader=1)
        shift_table = ShiftsTable.objects.filter(shift_no=request.POST['shift_no'])
     
        if groupleader and shift_table:
            groupleader = groupleader[0]
            groupleaderlineid = groupleader.line_id
            groupleader_empno = groupleader.emp_no
            shift = shift_table[0]

            if request.POST['change_date']:
                nowdate = request.POST['change_date']
            else:
                nowdate = datetime.now().strftime('%Y-%m-%d')

            punch_in = shift.punch_in
            new_punch_in = request.POST['punch_in']
            punch_out = shift.punch_out
            new_punch_out = request.POST['punch_out']
            # 時間文字加入當日改dt格式
            new_punch_in_dt = datetime.strptime(nowdate + new_punch_in, "%Y-%m-%d%H:%M")
            new_punch_out_dt = datetime.strptime(nowdate + new_punch_out, "%Y-%m-%d%H:%M")

            # 如果下班時間比上班早默認是隔天
            if new_punch_in_dt > new_punch_out_dt:
                new_punch_out_dt = new_punch_out_dt + timedelta(days=1)

            new_text = request.POST['text']
            if punch_in.strftime('%H:%M') != new_punch_in or punch_out.strftime('%H:%M') != new_punch_out:
                if request.POST['text'] == shift.text:
                    new_text = ("%s-%s(組長修改)，%s-%s(舊)，%s" % (
                        new_punch_in, new_punch_out, punch_in.strftime('%H:%M'), punch_out.strftime('%H:%M'), new_text))
                shift_table.update(text=new_text, punch_in=new_punch_in_dt, punch_out=new_punch_out_dt)
            else:
                shift_table.update(text=new_text)

            return redirect(request.META.get('HTTP_REFERER'))#回到提交前的網址

        else:
            groupleader = groupleader[0]
            groupleaderlineid = groupleader.line_id
            groupleader_empno = groupleader.emp_no

            if request.POST['change_date']:
                nowdate = request.POST['change_date']
            else:
                nowdate = datetime.now().strftime('%Y-%m-%d')

            new_punch_in = request.POST['punch_in']
            new_punch_out = request.POST['punch_out']


            # 時間文字加入當日改dt格式
            new_punch_in_dt = datetime.strptime(nowdate + new_punch_in, "%Y-%m-%d%H:%M")
            new_punch_out_dt = datetime.strptime(nowdate + new_punch_out, "%Y-%m-%d%H:%M")

            # 如果下班時間比上班早默認是隔天
            if new_punch_in_dt > new_punch_out_dt:
                new_punch_out_dt = new_punch_out_dt + timedelta(days=1)

            print(new_punch_in_dt)
            print(new_punch_out_dt)   

            new_text = request.POST['text']
            new_text= ("%s-%s(組長修改)，%s" % (
                new_punch_in, new_punch_out, new_text))

            ShiftsTableNotF.objects.create(
                shift_no="SH"+ request.POST['emp_no']+nowdate.replace("-",""),
                emp_no=request.POST['emp_no'],
                date=nowdate,
                text=new_text,
                punch_in=new_punch_in_dt,
                punch_out=new_punch_out_dt
            )

            return redirect(request.META.get('HTTP_REFERER'))#回到提交前的網址
            # return render(request, "change_shift_time.html")
    else:
        return render(request, "change_shift_time.html")



@require_http_methods(["POST"])
def change_shift_time_save(request):#廢棄，整合進change_shift_time一起
    if request.POST:
        emp_no = request.POST['groupleader']
        groupleader = ZzEmpTable.objects.filter(emp_no=emp_no, group_leader=1)
        shift_table = ShiftsTable.objects.filter(shift_no=request.POST['shift_no'])

        if groupleader and shift_table:
            groupleader = groupleader[0]
            groupleaderlineid = groupleader.line_id
            groupleader_empno = groupleader.emp_no
            shift = shift_table[0]

            nowdate = datetime.now()

            punch_in = shift.punch_in
            new_punch_in = request.POST['punch_in']
            punch_out = shift.punch_out
            new_punch_out = request.POST['punch_out']
            # 時間文字加入當日改dt格式
            new_punch_in_dt = datetime.strptime(str(nowdate.date()) + new_punch_in, "%Y-%m-%d%H:%M")
            new_punch_out_dt = datetime.strptime(str(nowdate.date()) + new_punch_out, "%Y-%m-%d%H:%M")

            # 如果下班時間比上班早默認是隔天
            if new_punch_in_dt > new_punch_out_dt:
                new_punch_out_dt = new_punch_out_dt + timedelta(days=1)

            new_text = request.POST['text']
            if punch_in.strftime('%H:%M') != new_punch_in or punch_out.strftime('%H:%M') != new_punch_out:
                if request.POST['text'] == shift.text:
                    new_text = ("%s-%s(組長修改)，%s-%s(舊)，%s" % (
                    new_punch_in, new_punch_out, punch_in.strftime('%H:%M'), punch_out.strftime('%H:%M'), new_text))
                shift_table.update(text=new_text, punch_in=new_punch_in_dt, punch_out=new_punch_out_dt)
            else:
                shift_table.update(text=new_text)

            emplist = ZzEmpTable.objects.filter(
                group_no=groupleader.group_no).values_list('emp_no', flat=True)
            emplist = list(emplist)
            shifts_view = shifts_attendance_view.objects.filter(
                date=nowdate, emp_no__in=emplist).values('emp_no', 'emp_name', 'shift_no', 'text', 'punch_in',
                                                         'punch_out', 'att_punch_in', 'att_punch_out')
            return render(request, "change_shift_time.html",
                          {'emp': shifts_view, 'groupleaderlineid': groupleaderlineid,
                           'groupleader_empno': groupleader_empno})
        else:
            return render(request, "change_shift_time.html")
    else:
        return render(request, "change_shift_time.html")
