from time import sleep
from public.smc import SMC
from public.btn import Btn
from public.glo import Glo
from public.log import log
from public.cutScreen import CScreen
from public.matchTem import Match

class Clean(object):
	"""docstring for Clean"""
	def __init__(self):
		super(Clean, self).__init__()
		self.name = Glo().get('name')
		CScreenOjb = CScreen()
		self.cutScreen = CScreenOjb.cutScreen
		self.customCutScreen = CScreenOjb.customCutScreen
		self.matchTem = Match().matchTem
		self.matchArrTem = Match().matchArrTem
		self.smc = SMC().smc
		self.smca = SMC().smca
		self.B = Btn()

	def start(self):
		try:
			while self.smc("hd", count=0) == 0:
				self.B.RBtn()

			self.B.Hotkey('bb')
			self.B.MBtn(710, 410)
			self.B.VBtn(1, 50)
			self.smc('bb_zl')
			self.smc('ck', sleepT=0.5)

			ckList = ['bb_qls', 'bb_bhs', 'bb_zqs', 'bb_xws', 'bb_tys', 'bb_yls', 'bb_sls', 'bb_fcs', 'bb_hbs', 'bb_kls']
			page = 1
			while True:
				self.customCutScreen('bb')
				res = self.matchArrTem(ckList)
				if res:
					Coor = ((513 + res[0][0], 202 + res[0][1]), res[1])
					self.B.LBtn(Coor, count=2, sleepT=1)
				else:
					self.B.MBtn(710, 410)
					self.B.VBtn(-1, 6)
					sleep(0.5)
					page+=1
					if page == 8 or self.smc('bb_empty'):
						self.B.RBtn()
						break
				if self.smc('bb_max', count=0):
					break
				

			self.B.Hotkey('bb')
			self.smc('bb_zl')
			self.B.MBtn(710, 410)
			self.B.VBtn(1, 50)
			sleep(0.5)

			syList = ['bb_sy1', 'bb_sy2', 'bb_sy3', 'bb_sy4', 'bb_sy5', 'bb_sy6', 'bb_sy7', 'bb_sy8', 'bb_sy9'] #'bb_jr'
			csList = ['bb_gms', 'bb_sms', 'bb_hws', 'bb_jt', 'bb_zzs', 'bb_zzs1', 'bb_zf']
			dqList = ['bb_dq1', 'bb_dq2', 'bb_dq_mj1', 'bb_dq_mj2', 'bb_dq_zz1', 'bb_dq_zz2', 'bb_dq_zz3', 'bb_dq_zz4', 'bb_dq_zz5', 'bb_dq_zz6', 'bb_hd_wz', 'bb_hd_piao'] # 'bb_dq_fu1', 'bb_dq_fu2', 'bb_dq_fu3', 
			page = 1
			while True:
				sy = self.smca(syList, count=2, sleepT=0.5)
				cs = self.smca(csList, simi=0.98, sleepT=0.5)
				if cs:
					self.smc('bb_gd', sleepT=0.5)
					self.smc('bb_smcs', sleepT=0.5)
					self.smc('bb_add_max', sleepT=0.5)
					self.smc('bb_cs', sleepT=0.5)
					sleep(0.5)
				dq = self.smca(dqList)
				if dq:
					self.smc('bb_dq', sleepT=0.5)
					self.smc('qd', sleepT=0.5)
				
				if not sy and not cs and not dq:
					self.B.MBtn(710, 410)
					self.B.VBtn(-1, 6)
					sleep(0.5)
					page+=1
					if page == 8 or self.smc('bb_empty'):
						self.B.RBtn()
						break

			log(f"账号：{ self.name } 背包清理完成")
			return 1
		except Exception as e:
			log(e, True)

if __name__ == '__main__':
	Clean().start()
