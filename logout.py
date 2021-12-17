from time import sleep
from public.smc import SMC
from public.btn import Btn
from public.glo import Glo
from public.log import log

class Logout(object):
	"""docstring for Logout"""
	def __init__(self):
		super(Logout, self).__init__()
		self.name = Glo().get('name')
		self.smc = SMC().smc
		self.B = Btn()

	def start(self, next):
		complete = False

		while True:
			res = self.smc('hd', count=0)
			if res == 0:
				self.B.RBtn()
			else:
				break

		if next:
			while True:
				self.B.Hotkey('xt')
				if not self.smc('hd', count=0):
					break

			xhList = ['qhzh', 'dc']
			while not complete:
				for item in xhList:
					res = self.smc(item)
					sleep(0.5)
					if res != 0 and item == 'dc':
						complete = True
						break

		else:
			complete = True

		if complete:
			log(f"账号: { self.name } 登出")
			return 1
		else:
			self.start()

if __name__ == '__main__':
	Logout().start()