# -- coding:utf-8--
import socket
import time
import datetime
import json
import os


def now_time():
	#用于获取当前时间的函数
	nowtime=datetime.datetime.now()
	timexx = nowtime.strftime('%Y-%m-%d-%H-%M')
	return timexx

def now_time_show():
	#用于获取当前时间的函数
	nowtime=datetime.datetime.now()
	timexx_show = nowtime.strftime('%Y-%m-%d-%H-%M-%S')
	return timexx_show


def wl_time(z):
	#生成未来时间的函数
	nowtime=datetime.datetime.now()
	detaday=datetime.timedelta(days=z)
	da_days=nowtime+detaday
	wltime = da_days.strftime('%Y-%m-%d-%H-%M')
	#输出返回值为 年 月 日 时 分
	return wltime

def userk_username_dzcdq(name):
	yzm = False
	userzclj = "userzc.json"

	with open(userzclj) as zx:
		userdzc = json.load(zx)
	if name in userdzc:
		yzm = True
	else:
		yzm = False

	return yzm


def userk_yz_qu():
	#用于取出userk信息的函数
	userklj = "userk.json"
	with open(userklj) as zx:
		userdzc = json.load(zx)
	return userdzc


def timeyz(tiz):
	yzjg = False
	timex = now_time()
	if tiz > timex:
		yzjg = True
	else:
		yzjg = False
	return yzjg

def userk_xr(mac,key,time):
	root = False
	x = "0"
	#用于添加用户的函数
	userklj = "userk.json"

	with open(userklj) as zx:
		userzd = json.load(zx)

	zhlb = [key,time,root,x]

	userzd[mac] = zhlb

	with open(userklj,'w') as ojbk_1:
		json.dump(userzd,ojbk_1)

def rm_userk_mac(mac):
	#用于删除用户信息的函数
	userklj = "userk.json"
	
	with open(userklj) as zx:
		userzd = json.load(zx)

	del userzd[mac]

	with open(userklj,'w') as ojbk_1:
		json.dump(userzd,ojbk_1)


def yzkey_keyk(key):
	#验证密钥库
	keyklj = "key.json"
	fhz = 0

	#打开密钥库
	with open(keyklj) as zx:
		keyk = json.load(zx)

	#判断密钥是否在密钥库中
	if key in keyk.keys():
		#获取密钥时间
		keytime = keyk[key]
		#将密钥时间转换为统一格式
		wl_time_sr = wl_time(keytime)
		#删除密钥库中的已用密钥
		del keyk[key]
		#写入到json文件中
		with open(keyklj,'w') as ojbk_1:
			json.dump(keyk,ojbk_1)
		fhz = "1"
		usertime = wl_time_sr
	else:
		fhz = "2"
		usertime = "0000-00-00-00-00"

	return fhz, usertime

def yzkey_userk_cz(mac):
	#验证用户信息库是否存在
	userklj = "userk.json"
	fhz = False
	#打开用户信息文件
	with open(userklj) as zx_1:
		userk = json.load(zx_1)
	#验证user是否存在
	if mac in userk.keys():
		ztm = True
	else:
		ztm = False
	return ztm


def yzkey_userk(key,mac):
	#验证用户信息库
	userklj = "userk.json"
	fhz = "0"
	#打开用户信息文件
	with open(userklj) as zx_1:
		userk = json.load(zx_1)
	#验证key是否存在
	if mac in userk.keys():
		user_xx = userk[mac]
		#取得用户预存密钥
		key = user_xx[0]
		time = user_xx[1]
		root = user_xx[2]
		x = user_xx[3]
		#查看时间是否有效
		if timeyz(time):
			ztm = "1"
		else:
			ztm = "3"
	else:
		ztm = "2"
		time = "0000-00-00-00-00"
		root = False
		x = "0"
	return ztm, time, root, x

def time_tjkey(key,mac):
	#用于延长卡密时间
	fhz = "0"
	#提取时间
	ztm, time = yzkey_keyk(key)
	if ztm == "2":
		fhz = "2"
	if ztm == "1":
		userklj = "userk.json"
		fhz = "0"
		#打开用户信息文件
		with open(userklj) as zx_1:
			userk = json.load(zx_1)
		user_xx = userk[mac]
		user_xx[1] = time
		userk[mac] = user_xx
		#写入到json文件中
		with open(userklj,'w') as ojbk_1:
			json.dump(userk,ojbk_1)
		fhz = "1"
	return fhz, time

def rzxr(rznr):
	hi = 'rz.txt'
	with open(hi,'a') as hii:
		hii.write(rznr)

def rzzl(mac, addr, show_time, time, x, yj):
	#日志写入
	addr_b = []
	for addr_z in addr:
		addr_e = str(addr_z)
		addr_b.append(addr_e)
	addr_a = " ".join(addr_b)
	rz_zc = show_time + "\n" + mac + "\n" + addr_a + "\n" + yj + "\n" + time + "\n" + x + "\n" + "\n"
	rzxr(rz_zc)