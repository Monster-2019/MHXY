import re
from time import sleep

from loguru import logger

from ocr import ocr


class Complex(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val

    def get_info(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        self.btn.hotkey('js')
        self.capture.custom_capture('name')
        name_level = ocr(f'./images/{self.capture.screen}.jpg')[0]
        self.btn.r()

        if name_level:
            match = re.match(r"(.+)(\d{2})", name_level)
            if match:
                name = match.group(1)
                level = int(match.group(2))

        sleep(0.5)

        self.btn.hotkey('bb')
        self.capture.custom_capture('gold')
        gold = ocr(f'./images/{self.capture.screen}.jpg')[0]

        sleep(0.5)

        self.capture.custom_capture('silver')
        silver = ocr(f'./images/{self.capture.screen}.jpg')[0]

        self.btn.r()

        logger.info(f"账号:{name}, 等级:{level}级, 金币:{gold}, 银币:{silver}")

        return {
            name: name,
            level: level,
            gold: gold,
            silver: silver,
        }

    def clean(self):
        while not self.smc('hd', isClick=False):
            self.btn.r()

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
                self.btn.l((coor[0] + 513, coor[1] + 202, coor[2], coor[3]))
                self.btn.l((coor[0] + 513, coor[1] + 202, coor[2], coor[3]))
                break
            else:
                self.btn.m(710, 410)
                self.btn.v(-1, 6)
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

    def singin(self):
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

    def get_hyd(self):
        while not self.smc('hd', isClick=False):
            self.btn.r()

        self.btn.hotkey('hd')

        hyd_list = []
        for coor in hyd_list:
            self.smc(coor, sleep_time=0.2)

        logger.info(f"账号: { self.name } 活跃度领取完成")

    def join_team_leader(self):
        while not self.smc('hd', isClick=False):
            self.btn.r()

        self.btn.hotkey('dw')

        self.smc('cjdw', sleep_time=0.5)

        self.smc('dw_sq')

        count = 0

        while True:
            accept = self.smc('dw_js')
            if accept:
                n += 1
            elif count >= 4:
                break

        self.btn.r()

    def join_team_player(self):
        while not self.smc('hd', isClick=False):
            self.btn.r()

        self.btn.hotkey('hy')
        self.smc('lxr')

        while True:
            self.capture()
            dz_x, dz_y = self.match('dz')
            if dz_x:
                x, y, w, h = self.match('jt', 'imgTem/dz')
                if coor:
                    coor = (dz_x + x, dz_y + y, w, h)
                    self.btn.l(coor, sleep_time=1)

                    if self.smc('sqrd') or self.smc('sqrd1'):
                        break

        self.btn.r()

    def leave_team(self):
        while not self.smc('hd', isClick=False):
            self.btn.r()

        self.btn.hotkey('dw')

        while True:
            self.smc('tcdw', sleep_time=1)
            if self.smc('cjdw', is_click=False):
                break

        self.btn.r()

    def task_finished(self, rw_list, type='rchd'):
        if isinstance(rw_list, str):
            rw_list = [rw_list]
        self.btn.hotkey('hd')

        self.smc(type, sleep_time=0.5)

        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        for i in range(31):
            if i % 10 == 0:
                sleep(0.5)
                for rw in rw_list:
                    result = self.smc(rw, is_click=False, simi=0.999)
                    if result:
                        return result

            self.btn.v(-1)

        self.btn.r()

        sleep(1)

        return False


if __name__ == '__main__':
    import win32gui
    from capture import CaptureScreen
    from match import Match
    from btn import Btn
    from smc import SMC

    hwnd = win32gui.FindWindow(None, "《梦幻西游》手游")
    screen = '0'
    capture = CaptureScreen(hwnd, screen)
    match = Match(screen)
    btn = Btn(hwnd)
    smc = SMC(capture, match, btn)

    adb = {
        'screen': screen,
        'hwnd': hwnd,
        'capture': capture,
        'match': match,
        'btn': btn,
        'smc': smc,
    }
    
    Complex(adb).singin()