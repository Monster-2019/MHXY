from datetime import datetime
WEEKDAY = datetime.today().isoweekday()
HOUR = datetime.today().hour
CJMY_STATUS = False
# if (WEEKDAY == 4 or WEEKDAY == 5) and HOUR >= 8:
    # CJMY_STATUS = True

DEFAULT_CLASS = '0'

ACCT_LIST = ['0', '1', '2', '3', '4']
# ACCT_LIST = ['0', '4']

ACCTIFNO_LIST = [
    [
        { 'acct': 'h1', 'server': 'zh1_z2', 'status': False, 'coor': ((30, 440), (500, 75)) },
        { 'acct': 'h2', 'server': 'zh2_z2', 'status': False, 'coor': ((30, 360), (500, 75)) },
        { 'acct': 'h3', 'server': 'zh3_z2', 'status': False, 'coor': ((30, 280), (500, 75)) },
        { 'acct': 'h4', 'server': 'zh4_z2', 'status': False, 'coor': ((30, 210), (500, 70)) },
        { 'acct': 'h5', 'server': 'zh5_z2', 'status': False, 'coor': ((30, 130), (500, 70)) }
    ],
    [
        { 'acct': 'h1', 'server': 'zh1_z3', 'status': False, 'coor': ((30, 440), (500, 75)) },
        { 'acct': 'h2', 'server': 'zh2_z3', 'status': False, 'coor': ((30, 360), (500, 75)) },
        { 'acct': 'h3', 'server': 'zh3_z3', 'status': False, 'coor': ((30, 280), (500, 75)) },
        { 'acct': 'h4', 'server': 'zh4_z3', 'status': False, 'coor': ((30, 210), (500, 70)) },
        { 'acct': 'h5', 'server': 'zh5_z3', 'status': False, 'coor': ((30, 130), (500, 70)) }
    ],
    [
        { 'acct': 'h1', 'server': 'zh1_z4', 'status': False, 'coor': ((30, 440), (500, 75)) },
        { 'acct': 'h2', 'server': 'zh2_z4', 'status': False, 'coor': ((30, 360), (500, 75)) },
        { 'acct': 'h3', 'server': 'zh3_z4', 'status': False, 'coor': ((30, 280), (500, 75)) },
        { 'acct': 'h4', 'server': 'zh4_z4', 'status': False, 'coor': ((30, 210), (500, 70)) },
        { 'acct': 'h5', 'server': 'zh5_z4', 'status': False, 'coor': ((30, 130), (500, 70)) }
    ]
]

ACCTZU = [
    {
        'status': True,
        'config': {
            'TeamStatus': False,
            'ZG_COUNT': 1,
            'ZG': True,
            "ZG_WC": None,
            'FB': True,
            'FB_WC': None,
            'CJMY': CJMY_STATUS,
            'NEXT': True
        },
        'acctList': ACCTIFNO_LIST[0]
    },
    {
        'status': True,
        'config': {
            'TeamStatus': False,
            'ZG_COUNT': 1,
            'ZG': True,
            "ZG_WC": None,
            'FB': True,
            'FB_WC': None,
            'CJMY': CJMY_STATUS,
            'NEXT': True
        },
        'acctList': ACCTIFNO_LIST[1]
    },
    {
        'status': True,
        'config': {
            'TeamStatus': False,
            'ZG_COUNT': 1,
            'ZG': True,
            "ZG_WC": None,
            'FB': True,
            'FB_WC': None,
            'CJMY': CJMY_STATUS,
            'NEXT': True
        },
        'acctList': ACCTIFNO_LIST[2]
    },
]

# {
    #     'config': {
    #         'TeamStatus': False,
    #         'ZG_COUNT': 1,
    #         'ZG': True,
    #         "ZG_WC": None,
    #         'FB': True,
    #         'FB_WC': None,
    #         'CJMY': False,
    #         'NEXT': True
    #     },
    #     'acctList': [
    #         {
    #             'acct': 'h1',
    #             'server': 'zh1_z1',
    #             'status': False,
    #             'menpai': 'pt',
    #             'coor': ((30, 440), (500, 75))
    #         },
    #         {
    #             'acct': 'h2',
    #             'server': 'zh2_z1',
    #             'status': False,
    #             'menpai': 'mw',
    #             'coor': ((30, 360), (500, 75))
    #         },
    #         {
    #             'acct': 'h3',
    #             'server': 'zh3_z1',
    #             'status': False,
    #             'menpai': 'st',
    #             'coor': ((30, 280), (500, 75))
    #         },
    #         {
    #             'acct': 'h4',
    #             'server': 'zh4_z1',
    #             'status': False,
    #             'menpai': 'df',
    #             'coor': ((30, 210), (500, 70))
    #         },
    #         {
    #             'acct': 'h5',
    #             'server': 'zh5_z1',
    #             'status': False,
    #             'menpai': 'fc',
    #             'coor': ((30, 130), (500, 70))
    #         }
    #     ]
    # },