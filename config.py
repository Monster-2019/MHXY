from datetime import datetime
GLOBAL_SIMI = 0.99

WEEKDAY = datetime.today().isoweekday()
HOUR = datetime.today().hour
CJMY_STATUS = False
# if (WEEKDAY == 4 or WEEKDAY == 5) and HOUR >= 8:
# CJMY_STATUS = True

ACCT_LIST = ['0', '1', '2', '3', '4']
# ACCT_LIST = ['0', '4']

ACCTIFNO_LIST = [
    [{
        'acct': 'h1',
        'server': 'zh1_z5',
        'status': False,
        'coor': 'zh1'
    }, {
        'acct': 'h2',
        'server': 'zh2_z5',
        'status': False,
        'coor': 'zh2'
    }, {
        'acct': 'h3',
        'server': 'zh3_z5',
        'status': False,
        'coor': 'zh3'
    }, {
        'acct': 'h4',
        'server': 'zh4_z5',
        'status': False,
        'coor': 'zh4'
    }, {
        'acct': 'h5',
        'server': 'zh5_z5',
        'status': False,
        'coor': 'zh5'
    }],
    [{
        'acct': 'h1',
        'server': 'zh1_z6',
        'status': False,
        'coor': 'zh1'
    }, {
        'acct': 'h2',
        'server': 'zh2_z6',
        'status': False,
        'coor': 'zh2'
    }, {
        'acct': 'h3',
        'server': 'zh3_z6',
        'status': False,
        'coor': 'zh3'
    }, {
        'acct': 'h4',
        'server': 'zh4_z6',
        'status': False,
        'coor': 'zh4'
    }, {
        'acct': 'h5',
        'server': 'zh5_z6',
        'status': False,
        'coor': 'zh5'
    }],
]

ACCTZU = [
    {
        'status': True,
        'config': {
            'TeamStatus': False,
            'ZG_COUNT': 2,
            'ZG': True,
            "ZG_WC": None,
            'FB': True,
            'FB_WC': None,
            'CJMY': CJMY_STATUS,
            'NEXT': False
        },
        'acctList': ACCTIFNO_LIST[0]
    },
    # {
    #     'status': False,
    #     'config': {
    #         'TeamStatus': False,
    #         'ZG_COUNT': 2,
    #         'ZG': True,
    #         "ZG_WC": None,
    #         'FB': False,
    #         'FB_WC': None,
    #         'CJMY': CJMY_STATUS,
    #         'NEXT': False
    #     },
    #     'acctList': ACCTIFNO_LIST[1]
    # },
    # {
    #     'status': True,
    #     'config': {
    #         'TeamStatus': False,
    #         'ZG_COUNT': 1,
    #         'ZG': True,
    #         "ZG_WC": None,
    #         'FB': True,
    #         'FB_WC': None,
    #         'CJMY': CJMY_STATUS,
    #         'NEXT': True
    #     },
    #     'acctList': ACCTIFNO_LIST[1]
    # },
]