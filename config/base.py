from datetime import datetime

GLOBAL_SIMI = 0.994

WEEKDAY = datetime.today().isoweekday()
HOUR = datetime.today().hour
CJMY_STATUS = False
# if (WEEKDAY == 4 or WEEKDAY == 5) and HOUR >= 8:
# CJMY_STATUS = True

ACCT_LIST = ["0", "1", "2", "3", "4"]
# ACCT_LIST = ['0']
