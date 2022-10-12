import win32gui

def hide():
    hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
    win32gui.ShowWindow(hwnd, 0) # 0 隐藏  1 显示

    return True

if __name__ == '__main__':
    hide()