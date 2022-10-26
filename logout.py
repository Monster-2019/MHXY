from time import sleep
from smc import SMC
from btn import Btn
from glo import Glo
from log import log
import win32gui, win32con
from win32 import win32process
import os

class Logout(object):
	"""docstring for Logout"""
	def __init__(self):
		super(Logout, self).__init__()
		self.glo = Glo()
		self.name = self.glo.get('name')
		self.smc = SMC().smc
		self.B = Btn()
		self.hwnd = self.glo.get('windowClass')

	def start(self, next):
		complete = True

		if next:
			thread_id, process_id = win32process.GetWindowThreadProcessId(self.hwnd)
			os.system('taskkill /f /pid %s' % str(process_id))

		# win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)

		# while True:
		# 	res = self.smc('hd', count=0)
		# 	if res == 0:
		# 		self.B.RBtn()
		# 	else:
		# 		break

		# if next:
		# 	while True:
		# 		self.B.Hotkey('xt')
		# 		if not self.smc('hd', count=0):
		# 			break

		# 	xhList = ['qhzh', 'dc']
		# 	while not complete:
		# 		for item in xhList:
		# 			res = self.smc(item)
		# 			sleep(0.5)
		# 			if res != 0 and item == 'dc':
		# 				complete = True
		# 				break

		# else:
		# 	complete = True

		if complete:
			log(f"账号: { self.name } 登出")
			return 1
		else:
			self.start()

if __name__ == '__main__':
	Logout().start()