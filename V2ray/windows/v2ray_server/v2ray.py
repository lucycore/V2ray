# -- coding:utf-8--
import socket
import time
import datetime
import json
import os
import mods

#声明主机
host = ""
#声明端口号
port = 2233
#创建sock套接字
sock = socket.socket()
#绑定主机和端口
sock.bind((host, port))
#开始监听
sock.listen(5)
#对话循环

print("v2ray server start！")

while True:
    try:
        #堵塞连接
        cli, addr = sock.accept()
        #打印连接pi及信息
        show_time = mods.now_time_show()
        print("")
        print(addr)
        print(show_time)
        #接收密钥
        data = cli.recv(2048).decode()
        key = data
        #验证密钥
        sen_zt, sen_time = mods.yzkey(key)
        #发送回客户端
        cli.sendall(sen_zt.encode())
        time.sleep(1)
        cli.sendall(sen_time.encode())
        if sen_zt == "1" :
            print("ok")
        else:
            if sen_zt == "2" :
                print("key_no")
            else:   
                if sen_zt == "3" :
                    print("no_key")
                else:
                    print("哈？")
        print("")
        #关闭连接
        cli.close()
    except:
        show_time = mods.now_time_show()
        print("\n错误！")
        print(show_time)
        print("\n")