from time import sleep
from public.smc import SMC
from public.btn import Btn

class Clean(object):
	"""docstring for Clean"""
	def __init__(self):
		super(Clean, self).__init__()
		self.smc = SMC().smc
		self.B = Btn()

	def start(self):
		while True:
			res = self.smc('hd', count=0)
			if res == 0:
				self.B.RBtn()
			else:
				break

		self.B.Hotkey('bb')
		self.B.MBtn(710, 410)
		self.B.VBtn(1, 30)
		self.smc('bb_zl')

		self.smc('ck', sleepT=0.5)
		ckList = ['bb_qls', 'bb_bhs', 'bb_zqs', 'bb_xws', 'bb_gms', 'bb_tys', 'bb_yls', 'bb_sls', 'bb_fcs', 'bb_hbs', 'bb_hws', 'bb_sms', 'bb_kls']
		page = 0

		while True:
			res = self.smc(ckList, simi=0.9, infoKey='bb', count=2, sleepT=0.5)
			rs = self.smc('bb_max', count=0)
			if rs == 1:
				break
			if res == 0:
				self.B.MBtn(710, 410)
				self.B.VBtn(-1, 6)
				page+=1
				if page == 5:
					break

		self.B.RBtn()
		self.B.Hotkey('bb')
		self.smc('bb_zl')
		self.B.MBtn(710, 410)
		self.B.VBtn(1, 30)
		sleep(1)

		page = 0
		while True:
			res = self.smc('bb_jt', sleepT=0.5)
			if res == 1:
				self.smc('bb_smcs', sleepT=0.5)
				self.smc('bb_add', count=2, sleepT=0.5)
				self.smc('bb_cs', sleepT=0.5)
				self.smc('bb_zl', sleepT=0.5)
				sleep(1)
			else:
				self.B.MBtn(710, 410)
				self.B.VBtn(-1, 6)
				page+=1
				if page == 5:
					break

		self.B.MBtn(710, 410)
		self.B.VBtn(1, 30)
		sleep(1)

		page = 0
		while True:
			res = self.smc('bb_zzs', simi=0.8, sleepT=0.5)
			if res == 1:
				self.smc('bb_smcs', sleepT=0.5)
				self.smc('bb_cs', sleepT=0.5)
				self.smc('bb_zl', sleepT=0.5)
				sleep(1)
			else:
				self.B.MBtn(710, 410)
				self.B.VBtn(-1, 6)
				page+=1
				if page == 5:
					break

		self.B.MBtn(710, 410)
		self.B.VBtn(1, 30)
		sleep(1)

		page = 0
		while True:
			res = self.smc('bb_dq1') or self.smc('bb_zz')
			if res == 1:
				self.smc('bb_dq', sleepT=0.5)
				self.smc('qd', sleepT=0.5)
				self.smc('bb_zl', sleepT=0.5)
				sleep(1)
			else:
				self.B.MBtn(710, 410)
				self.B.VBtn(-1, 6)
				page+=1
				if page == 5:
					break

		self.B.RBtn()

		return 1

if __name__ == '__main__':
	Clean().start()
