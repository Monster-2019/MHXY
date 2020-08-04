from time import sleep
from public.smc import SMC
from public.btn import Btn

class Logout(object):
	"""docstring for Logout"""
	def __init__(self):
		super(Logout, self).__init__()
		self.smc = SMC().smc
		self.B = Btn()

	def start(self, next):
		complete = False

		while True:
			res = self.smc('hd', count=0)
			if res == 0:
				self.B.RBtn()
				sleep(1)
			else:
				break

		if next:
			self.B.Hotkey('xt')

			xhList = ['qhzh', 'dc']
			while not complete:
				for item in xhList:
					res = self.smc(item)
					if res == 1:
						if item == 'dc':
							complete = True
							break
		else:
			complete = True

		if complete:
			return 1
		else:
			self.start()

if __name__ == '__main__':
	Logout().start()