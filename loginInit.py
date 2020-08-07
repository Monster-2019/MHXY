import win32gui, win32ui, win32con, win32api, win32com.client
import os
from time import sleep
from public.glo import Glo
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.log import log

def loginInit():
    os.system('start D:\\Game\\梦幻西游手游\\My\\myLauncher.exe')
    sleep(3)
    os.system('start D:\\software\\dnplayer2\\dnplayer.exe')
    sleep(3)
    while True:
        tem = win32gui.FindWindow(None, '雷电模拟器')
        hwnd = win32gui.FindWindowEx(tem, None, 'RenderWindow', None)
        if hwnd != 0:
            break
    os.system('taskkill /F /IM mymain.exe')
    os.system('taskkill /F /IM dnplayer.exe')

if __name__ == "__main__":
    loginInit()