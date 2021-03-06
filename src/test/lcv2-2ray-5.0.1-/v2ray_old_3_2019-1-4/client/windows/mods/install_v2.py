# -- coding:utf-8--
import os
import zipfile
from urllib import request


def remove_dir(dir):
    #用于删除路径的函数
    dir = dir.replace('\\', '/')
    if(os.path.isdir(dir)):
        for p in os.listdir(dir):
            remove_dir(os.path.join(dir,p))
        if(os.path.exists(dir)):
            os.rmdir(dir)
    else:
        if(os.path.exists(dir)):
            os.remove(dir)

def d_v2_s():
    lj = r"C:\pythonz5"
    remove_dir(lj)


def Schedule(a,b,c):
    #显示进度的函数
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' %(per))


def t_v2():
    aaa = []
    test_re = True
    #用于测试程序是否安装的函数

    file_dir = r"C:\pythonz5"
    for x_b, _c, files in os.walk(file_dir):
        for x in files:
            aaa.append(x)
    bbb = ['V.zip', 'geoip.dat', 'geosite.dat', 'readme.md', 'v2ctl.exe', 'v2ctl.exe.sig', 'v2ray.exe', 'v2ray.exe.sig', 'wv2ray.exe', 'wv2ray.exe.sig']
    for x in bbb:
        if x in aaa:
            test_re = True
        else:
            test_re = False
            break
    return test_re



def addlj():

    mblj_1 = r'C:\pythonz5\sun36x64'
    mblj_2 = r'C:\pythonz5\unsers'
    #创建路径的函数
    os.makedirs(mblj_1)
    os.makedirs(mblj_2)



def get_v2ray():

    #v2ray服务器压缩包
    v2ray_server_rar_lj = "http://60.205.221.103/v2ray/v2rayWin.zip"
    #v2ray本地压缩包
    v2ray_rar_lj = r"C:\pythonz5\sun36x64\V.zip"
    v2ray_rar_jy_lj = r"C:\pythonz5\sun36x64"
    print("正在下载V2ray资源包\n")
    print("这需要几分钟时间\n")
    #下载压缩包
    request.urlretrieve(v2ray_server_rar_lj, v2ray_rar_lj, Schedule)
    print("已下载完成压缩包")
    azip = zipfile.ZipFile(v2ray_rar_lj)
    #解压到原始目录
    azip.extractall(v2ray_rar_jy_lj)
    print("已解压完成")
    input("按下回车继续！")

