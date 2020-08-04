# 
#    文件名批量处理
# 

import os
import shutil

path = "C:\\Users\\dongx\\Desktop\\mhxyScript\\images\\huan\\"
newpath = "C:\\Users\\dongx\\Desktop\\mhxyScript\\images\\imgTem\\"
def changeName():
    files = os.listdir(path)
    for file in files:
        name = file.split('.')
        oldName = path + file
        tem = 'h_' + name[0] + '.' + name[1]
        newname = path + tem
        os.rename(oldName, newname)

def moveFile():
    files = os.listdir(path)
    for file in files:
        src_name = os.path.join(path, file)
        tag_name = os.path.join(newpath, file)
        shutil.move(src_name, tag_name)
        print(f"{file}移动完成")

if __name__ == "__main__":
    changeName()
    moveFile()
    