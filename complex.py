from time import sleep

from loguru import logger


class Complex(object):

    def __init__(self, capture, match, btn, smc):
        self.capture = capture
        self.match = match
        self.btn = btn
        self.smc = smc

    def getInfo(self):
        while not self.smc('hd', isClick=False):
            self.B.RBtn()

        self.btn.hotkey('js')
        self.btn.r()

        pass

    def clean(self):
        while not self.smc('hd', isClick=False):
            self.B.RBtn()

        self.btn.hotkey('bb')
        self.btn.m(710, 410)
        self.btn.v(1, 50)
        self.smc('bb_zl')
        self.smc('ck', sleep_time=0.5)

        ck_list = [
            'bb_qls', 'bb_bhs', 'bb_zqs', 'bb_xws', 'bb_tys', 'bb_yls',
            'bb_sls', 'bb_fcs', 'bb_hbs', 'bb_kls'
        ]
        page = 1
        while True:
            self.capture.custom_capture()
            coor = self.match.match_tem_list(ck_list)
            if coor:
                self.btn.l(coor[0] + 513, coor[1] + 202, coor[2], coor[3])
                self.btn.l(coor[0] + 513, coor[1] + 202, coor[2], coor[3])
                break
            else:
                self.btn.MBtn(710, 410)
                self.btn.VBtn(-1, 6)
                sleep(0.5)
                page += 1
                if page == 8:
                    break

        self.smc('bb_zl')
        self.btn.m(710, 410)
        self.btn.v(1, 50)

        use_list = [
            'bb_sy1', 'bb_sy2', 'bb_sy3', 'bb_sy4', 'bb_sy5', 'bb_sy6',
            'bb_sy7', 'bb_sy8', 'bb_sy9'
        ]  #'bb_jr'
        sell_list = [
            'bb_gms', 'bb_sms', 'bb_hws', 'bb_jt', 'bb_zzs', 'bb_zzs1', 'bb_zf'
        ]
        dq_list = [
            'bb_dq1', 'bb_dq2', 'bb_dq_mj1', 'bb_dq_mj2', 'bb_dq_zz1',
            'bb_dq_zz2', 'bb_dq_zz3', 'bb_dq_zz4', 'bb_dq_zz5', 'bb_dq_zz6',
            'bb_hd_wz', 'bb_hd_piao'
        ]  # 'bb_dq_fu1', 'bb_dq_fu2', 'bb_dq_fu3',

        page = 1

        while True:
            self.capture()
            use = self.match.match_tem_list(use_list)
            if use:
                self.btn.l(use)
                self.btn.l(use)

            sell = self.match.match_tem_list(sell_list)
            if sell:
                self.smc('bb_gd', sleep_time=0.5)
                self.smc('bb_smcs', sleep_time=0.5)
                self.smc('bb_add_max', sleep_time=0.5)
                self.smc('bb_cs', sleep_time=0.5)

            dq = self.match.match_tem_list(dq_list)
            if dq:
                self.smc('bb_dq', sleep_time=0.5)
                self.smc('qd', sleep_time=0.5)

            if not use and not sell and not dq:
                self.btn.m(710, 410)
                self.btn.v(-1, 6)
                sleep(0.5)
                page += 1
                if page == 8:
                    self.btn.r()
                    break

        logger.info(f"清理完成")

    def guajiang(self):
        self.btn.hotkey('fl')

        self.smc('fl_mrfl', sleep_time=0.5)
        self.smc('fl_dkggl', sleep_time=0.5)

        self.btn.d((533, 396), (850, 485))

        reward_list = [(655, 567, 66, 66), (550, 567, 66, 66),
                       (760, 567, 66, 66), (865, 567, 66, 66)]

        for coor in reward_list:
            self.btn.l(coor, sleep_time=0.5)

            self.smc('sygb', sleep_time=0.3)

        self.btn.r()

        logger.info(f"刮奖完成")

    def lq_hyd(self):
        while not self.smc('hd', isClick=False):
            self.B.RBtn()

        self.btn.hotkey('hd')

        hyd_list = []
        for coor in hyd_list:
            self.smc(coor, sleep_time=0.2)

        pass

        logger.info(f"账号: { self.name } 活跃度领取完成")
        


if __name__ == '__main__':
    Complex().smc('bt_wc')