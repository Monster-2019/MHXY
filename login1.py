import win32gui, win32con, win32api, win32com.client
from loguru import logger
import os

SHELL = win32com.client.Dispatch("WScript.Shell")


def SetForegroundWindowMy(hwnd):
    SHELL.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)


def mnqInit():
    pass


def login(group, hwndList):
    login_list = []
    for hwnd in hwndList:
        SetForegroundWindowMy(hwnd)
        login_hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
        not_logged = win32gui.IsWindowVisible(login_hwnd)
        if hwnd and not_logged:
            login_list.append(hwnd)

    if len(login_list) == 5:
        mnqInit()
    else:
        logger.info('存在不同登录态，请检查')
        return os._exit()