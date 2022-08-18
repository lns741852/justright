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