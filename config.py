from datetime import datetime

GLOBAL_SIMI = 0.994

WEEKDAY = datetime.today().isoweekday()
HOUR = datetime.today().hour
CJMY_STATUS = False
# if (WEEKDAY == 4 or WEEKDAY == 5) and HOUR >= 8:
# CJMY_STATUS = True

ACCT_LIST = ["0", "1", "2", "3", "4"]
# ACCT_LIST = ['0']


ACCTZU = [
    {
        "status": True,
        "config": {
            "TeamStatus": False,
            "ZG_COUNT": 2,
            "ZG": True,
            "ZG_WC": None,
            "FB": True,
            "FB_WC": None,
            "NEXT": False,
        },
        "acctList": [
            {"server": "zh1_z8", "status": False, "account": "zh1"},
            {"server": "zh2_z8", "status": False, "account": "zh2"},
            {"server": "zh3_z8", "status": False, "account": "zh3"},
            {"server": "zh4_z8", "status": False, "account": "zh4"},
            {"server": "zh5_z8", "status": False, "account": "zh5"},
        ]
    }
]
