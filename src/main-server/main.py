# -- coding:utf-8--
#this file set in the main server
import threading
import socket
import time
import datetime
import json
import os
import uuid
import sys
import base64

this_program_use_to_sell = True
this_program_ID = ""
certificate_state = False

state = 0
#用于描述线程状态

def getVmess(username,ip,uuid):
	a = '''{
	"v": "2",
	"ps": "Lcv2_7.1_'''
	a2 = username
	a3 = '''",
	"add": "'''
	b = ip
	c = '''",
	"port": "26373",
	"id": "'''
	d = uuid
	e = '''",
	"aid": "10",
	"net": "tcp",
	"type": "http",
	"host": "www.baidu.com",
	"path": "",
	"tls": ""
	}'''
	data = a + a2 + a3 + b + c + d + e
	data = data.encode("utf-8")
	data = base64.b64encode(data)
	data = str(data)
	data = data[2:-1]
	data = "vmess://" + data
	return data

def get_Lcv2_config():
	global this_program_ID
	print("\n启动之前，需要您提供您的程序ID")
	print("用于标记，记录您的程序流量费用")
	print("为了避免错误，请不要使用汉字\n")
	this_program_ID = input("Program_ID：")

def send_traffic_to_S_control(trafficG):
	#此函数在程序为出售时被激活
	#用于发送用户流量添加情况
	HOST = "ahhhhhh.top"
	PORT = 5897
	sock = socket.socket()
	sock.connect((HOST, PORT))
	data = this_program_ID + "*data*" + trafficG
	sock.sendall(data.encode())
	my = sock.recv(10240).decode()

def test_program_certificate():
	#此函数在程序为出售时被激活
	#用于验证此程序的运行是否合法
	HOST = "ahhhhhh.top"
	PORT = 5896
	sock = socket.socket()
	sock.connect((HOST, PORT))
	sock.sendall(this_program_ID.encode())
	certificate = sock.recv(10240).decode()
	if certificate == "True":
		return True
	else:
		return False



def error_print(data):
	#错误反馈打印函数
	datalist = data.split("*data*")
	for e in datalist:
		print(e)


class UserData():
	#用于操作用户数据json的类

	def __init__(self,ip="",email="",uuid="",traffic=""):
		self.path = "userdata.json"
		self.ip = ip
		self.email = email
		self.uuid = uuid
		self.traffic = traffic
		self.userdata = {}


	def readUserData(self):
		try:
			with open(self.path) as zx:
				userdata = json.load(zx)
				self.userdata = userdata
		except Exception as e:
			print(e)
			print("\n\nUserData类内部错误！！")
			print("读取用户数据库失败！\n\n")


	def writeUserData(self):
		try:
			with open(self.path,'w') as ojbk:
				json.dump(self.userdata,ojbk)
		except Exception as e:
			print(e)
			print("\n\nUserData类内部错误！！")
			print("写入用户数据库失败！\n\n")


	def addUser(self):
		try:
			one_user_data_list = [self.email,self.uuid,self.traffic]
			self.userdata[self.ip].append(one_user_data_list)
		except Exception as e:
			print(e)
			print("\n\nUserData类内部错误！！")
			print("添加用户到指定的ip下失败！\n\n")


	def delUser(self):
		sonserver_users = self.userdata[self.ip]
		
		user_index = 0
		find_state = False
		userUuid = ""
		for one_user_data in sonserver_users:
			if one_user_data[0] == self.email:
				find_state = True
				userUuid = one_user_data[1]
				break
			else:
				user_index += 1

		if find_state :
			del self.userdata[self.ip][user_index]

		else:
			print("\n\nUserData类内部错误！！")
			print("在用户数据库之中没有找到要删除的用户！\n\n")

		return userUuid


	def addServer(self):
		try:
			self.userdata[self.ip] = []
		except Exception as e:
			print(e)
			print("\n\nUserData类内部错误！！")
			print("添加服务器到用户数据库失败！\n\n")


	def delServer(self):
		try:
			del self.userdata[self.ip]
		except Exception as e:
			print(e)
			print("\n\nUserData类内部错误！！")
			print("删除服务器在用户数据库中失败！\n\n")


	def addTraffic(self):
		#添加流量需要提供ip下用户邮箱以及添加的流量数额
		try:
			userlist = self.userdata[self.ip]
			user_index = 0
			state = False
			for one_user in userlist:
				if one_user[0] == self.email:
					traffic = int(userlist[user_index][2])\
						 + int(self.traffic)
					userlist[user_index][2] = str(traffic)
					state = True
					break
				user_index += 1
			if state == False:
				print("\n\nUserData类内部错误！！")
				print("没有找到要添加流量的用户！\n\n")

		except Exception as e:
			print(e)
			print("\n\nUserData类内部错误！！")
			print("添加流量到用户出错！\n\n")


	def delTraffic(self):
		#删除流量需要提供ip下用户邮箱以及删除的流量数额
		try:
			userlist = self.userdata[self.ip]
			user_index = 0
			state = False

			for one_user in userlist:
				if one_user[0] == self.email:
					traffic = int(userlist[user_index][2])\
						 - int(self.traffic)
					userlist[user_index][2] = str(traffic)
					state = True
					break
				user_index += 1
			if state == False:
				print("\n\nUserData类内部错误！！")
				print("没有找到要删除流量的用户！\n\n")

		except Exception as e:
			print(e)
			print("\n\nUserData类内部错误！！")
			print("删除流量到用户出错！\n\n")


	def getUserDetails(self):
		try:
			return self.userdata
		except Exception as e:
			print(e)
			print("\n\nUserData类内部错误！！")
			print("返回用户信息细节失败！\n\n")


	def getIp(self):
		number = 0
		for ip, _ in self.userdata.items():
			number += 1
			if str(number) == self.ip:
				return ip


class Lcv2_Socket():

	def __init__(self,ip="",email="",uuid="",time=10):
		self.ip = ip
		self.email = email
		self.uuid = uuid
		self.sock = socket.socket()
		self.sock.settimeout(time)


	def connectServer(self):
		HOST = self.ip
		PORT = 2233
		self.sock.connect((HOST, PORT))
		

	def addLcv2User(self):
		#用于添加用户的函数

		dataList = ["add_user",self.email,self.uuid]
		data = '*data*'.join(dataList)

		self.sock.sendall(data.encode())
		serverRecv = self.sock.recv(10240).decode()

		if serverRecv == "True":
			return "True"
		else:
			error_print(serverRecv)
			return "False"


	def delLcv2User(self):
		#用于删除用户的函数
		
		dataList = ["del_user",self.email,self.uuid]
		data = '*data*'.join(dataList)

		self.sock.sendall(data.encode())
		serverRecv = self.sock.recv(10240).decode()

		if serverRecv == "True":
			return "True"
		else:
			error_print(serverRecv)
			return "False"


	def readLcv2User(self):
		#用于读取用户流量使用情况的函数

		dataList = ["read_user",self.email]
		data = '*data*'.join(dataList)

		self.sock.sendall(data.encode())
		serverRecv = self.sock.recv(10240).decode()

		try:
			serverRecv = int(serverRecv)
			return True, serverRecv
		except Exception as e:
			print(e)
			error_print(serverRecv)
			return False, "0"


	def closeConnect(self):
		self.sock.close()


def mainService():
	#用于服务器自动化删除流量耗尽用户
	print("流量消耗更新服务开启")
	global certificate_state

	if certificate_state == True:

		data = UserData()
		data.readUserData()
		userdata = data.getUserDetails()
		for server_ip, users in userdata.items():
			for one_user in users:
				try:
					lcv2Sock = Lcv2_Socket(time=5)
					print("\n查找用户：" + one_user[0])
					lcv2Sock.ip = server_ip
					lcv2Sock.email = one_user[0]
					lcv2Sock.connectServer()
					state, traffic = lcv2Sock.readLcv2User()
					lcv2Sock.closeConnect()
				except Exception as e:
					print(e)
					print("服务器抓取错误！")
					state = False

				if state== True and traffic != "0":
					data.ip = server_ip
					data.email = one_user[0]
					data.traffic = traffic
					data.delTraffic()
					print("用户: " + one_user[0] + " 查找成功")
					print("删除流量：" + str(traffic))
				else:
					print("错误！没有找到用户："+one_user[0])
		
		data.writeUserData()
		print("用户信息更新完成！")

		print("正在执行清除流量耗尽用户行为")
		userdata = data.getUserDetails()
		lcv2Sock = Lcv2_Socket()

		for server_ip, users in userdata.items():
			for one_user in users:
				if int(one_user[2]) == 0 or int(one_user[2]) < 0:
					print("发现过期用户："+one_user[0])
					data.ip = server_ip
					data.email = one_user[0]
					data.delUser()

					lcv2Sock.ip = server_ip
					lcv2Sock.email = one_user[0]
					lcv2Sock.uuid = one_user[1]
					lcv2Sock.connectServer()
					state = lcv2Sock.delLcv2User()
					lcv2Sock.closeConnect()
					if state == "True":
						print("成功！")
					else:
						error_print(state)
						print("错误！")

		data.writeUserData()
		print("清除行为完成！")

	if this_program_use_to_sell:
		print("正在验证程序证书")
		print("\n\nLcv2 程序证书验证")
		if test_program_certificate():
			print("您的证书有效！")
			print("您的程序ID：" + this_program_ID)
			certificate_state = True
		else:
			print("您的证书已失效！")
			print("您的程序ID：" + this_program_ID)
			print("请立即联系您的程序管理员！")
			print("20秒之后您的所有子服务器将会关闭！")
			print("如需恢复子服务器，请初始化子服务器！")
			certificate_state = False

			data = UserData()
			data.readUserData()
			data = data.getUserDetails()
			for server_ip , userlist in data.items():
				for one_user in userlist:
					sock = Lcv2_Socket()
					sock.ip = server_ip
					sock.email = one_user[0]
					sock.uuid = one_user[1]
					sock.connectServer()
					sock.delLcv2User()	
					sock.closeConnect()


def dataControl(cmd):
	#cmd命令控制程序
	if cmd[0] == "h":
		print("\nLcv2 信息主控使用帮助(ip为服务器编号,tip为整个ip)（自动保存）")
		print("au [ip] [email] [traffic] 添加用户到服务器下")
		print("du [ip] [email] 删除用户在服务器下")
		print("tu [ip] [email] [newIp] 转移用户到新的服务器")
		print("ptu [tip] [newtIp] 转移所有指定用户到新的服务器")
		print("at [ip] [email] [traffic] 添加用户流量")
		print("dt [ip] [email] [traffic] 删除用户流量")
		print("initusdata 初始化用户信息文件")#
		print("initserver 进行服务器初始化")
		print("ud 更新用户流量数据 ")
		print("as [tip] 添加服务器")
		print("ds [ip] 删除服务器")
		print("gvm [ip] [email] 获取用户vmess链接")
		print("pgvm [ip] 批量获取用户vmess链接\n")
		print("q  强制退出程序")
		print("lst  列出所有子进程")
		print("---------信息查找浏览分类---------")
		print("la 列出所有用户信息")
		print("ls 列出所有服务器信息")
		print("lu [ip] 列出指定ip下的所有用户")
		print("fu [email] 查询指定用户在所有ip下")
		print("wt 延迟主进程更新时间")

	elif cmd[0] == "pgvm":
		print("正在获取用户vmess")
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		serverip = data.getIp()
		userdata = data.getUserDetails()
		for ip, userlist in userdata.items():
			if serverip == ip:
				for one_user in userlist:
					vmess = getVmess(one_user[0],serverip,one_user[1])
					print("\n用户名称：" + one_user[0])
					print("信息码：")
					print(vmess)
					input("输入回车继续")
		print("完成")


	elif cmd[0] == "ptu":
			print("用户转移模式")
			data = UserData()
			data.readUserData()
			data = data.getUserDetails()
			#获取用户信息
			for ip, UserList in data.items():
				if ip == cmd[1]:
					for oneUserData in UserList:

						print("用户信息")
						print(oneUserData)
						#加入到新的数据结构
						data = UserData()
						data.readUserData()
						data.ip = cmd[2]
						data.email = oneUserData[0]
						data.uuid = oneUserData[1]
						data.traffic = oneUserData[2]
						data.addUser()
						data.writeUserData()
						print("新服务器数据库加入完成")
						#删除用户在旧的数据
						data = UserData()
						data.readUserData()
						data.ip = ip
						data.email = oneUserData[0]
						_ = data.delUser()
						data.writeUserData()
						print("旧数据删除完成")
						#加入到新的子服务器
						sock = Lcv2_Socket()
						sock.ip = cmd[2]
						sock.email = oneUserData[0]
						sock.uuid = oneUserData[1]
						sock.connectServer()
						sock.addLcv2User()
						sock.closeConnect()
						print("加入新子服务器完成")

						#删除用户在久的子服务器
						try:
							sock = Lcv2_Socket()
							sock.ip = ip
							sock.email = oneUserData[0]
							sock.uuid = oneUserData[1]
							sock.connectServer()
							sock.delLcv2User()
							sock.closeConnect()
						except Exception as e:
							print(e)
						print("移除旧子服务器完成")

						print("完成")


	elif cmd[0] == "tu":
		print("用户转移模式")
		userOneData = []
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		serverip = data.getIp()
		data = data.getUserDetails()
		#获取用户信息
		for userOneLine in data[serverip]:
			if userOneLine[0] == cmd[2]:
				userOneData = userOneLine[:]
		print("用户信息")
		print(userOneData)
		#加入到新的数据结构
		data = UserData()
		data.readUserData()
		data.ip = cmd[3]
		nserverip = data.getIp()
		data.ip = nserverip
		data.email = userOneData[0]
		data.uuid = userOneData[1]
		data.traffic = userOneData[2]
		data.addUser()
		data.writeUserData()
		print("新服务器数据库加入完成")
		#删除用户在旧的数据
		data = UserData()
		data.readUserData()
		data.ip = serverip
		data.email = userOneData[0]
		_ = data.delUser()
		data.writeUserData()
		print("旧数据删除完成")
		#加入到新的子服务器
		sock = Lcv2_Socket()
		sock.ip = nserverip
		sock.email = userOneData[0]
		sock.uuid = userOneData[1]
		sock.connectServer()
		sock.addLcv2User()
		sock.closeConnect()
		print("加入新子服务器完成")

		#删除用户在久的子服务器
		try:
			sock = Lcv2_Socket()
			sock.ip = serverip
			sock.email = userOneData[0]
			sock.uuid = userOneData[1]
			sock.connectServer()
			sock.delLcv2User()
			sock.closeConnect()
		except Exception as e:
			print(e)
		print("移除旧子服务器完成")

		print("完成")


	elif cmd[0] == "au":
		print("添加用户模式")
		uuidd = str(uuid.uuid4())
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		serverip = data.getIp()
		data.ip = serverip
		data.email = cmd[2]
		data.uuid = uuidd
		data.traffic = cmd[3]
		data.addUser()
		data.writeUserData()

		sock = Lcv2_Socket()
		sock.ip = serverip
		sock.email = cmd[2]
		sock.uuid = uuidd
		sock.connectServer()
		sock.addLcv2User()
		sock.closeConnect()
		if this_program_use_to_sell:
			send_traffic_to_S_control(cmd[3])
		print("完成")

	elif cmd[0] == "du":
		print("删除用户模式")
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		serverip = data.getIp()
		data.ip = serverip
		data.email = cmd[2]
		userUid = data.delUser()
		data.writeUserData()

		sock = Lcv2_Socket()
		sock.ip = serverip
		sock.email = cmd[2]
		sock.uuid = userUid
		sock.connectServer()
		sock.delLcv2User()
		sock.closeConnect()
		print("完成")

	elif cmd[0] == "at":
		print("添加用户流量模式")
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		serverip = data.getIp()
		data.ip = serverip
		data.email = cmd[2]
		data.traffic = cmd[3]
		data.addTraffic()
		data.writeUserData()
		if this_program_use_to_sell:
			send_traffic_to_S_control(cmd[3])
		print("完成")
		

	elif cmd[0] == "dt":
		print("删除用户流量模式")
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		serverip = data.getIp()
		data.ip = serverip
		data.email = cmd[2]
		data.traffic = cmd[3]
		data.delTraffic()
		data.writeUserData()
		print("完成")

	elif cmd[0] == "initserver":
		data = UserData()
		data.readUserData()
		data = data.getUserDetails()
		for server_ip , userlist in data.items():
			for one_user in userlist:
				sock = Lcv2_Socket()
				sock.ip = server_ip
				sock.email = one_user[0]
				sock.uuid = one_user[1]
				sock.connectServer()
				sock.addLcv2User()	
				sock.closeConnect()
		

	elif cmd[0] == "ud":
		mainService()

	elif cmd[0] == "as":
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		data.addServer()
		data.writeUserData()

	elif cmd[0] == "ds":
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		serverip = data.getIp()
		data.ip = serverip
		data.delServer()
		data.writeUserData()

	elif cmd[0] == "la":
		print("\n全部用户信息查询模式")
		data = UserData()
		data.readUserData()
		data = data.getUserDetails()
		number = 0
		for ip, userlist in data.items():
			number += 1
			number2 = 0 
			print("编号：" + str(number) + "  服务器ip：" + ip)
			for one_user in userlist:
				number2 += 1
				print("\n  编号：" + str(number2))
				print("  用户："+ one_user[0])
				print("  uuid："+ one_user[1])
				print("  流量剩余："+ one_user[2])
		

	elif cmd[0] == "ls":
		print("\n服务器信息查询模式\n")
		data = UserData()
		data.readUserData()
		data = data.getUserDetails()
		number = 0
		for ip, userlist in data.items():
			number += 1
			print("编号：" + str(number) + "  服务器ip：" + ip\
				+ " 用户数量：" + str(len(userlist)))
		

	elif cmd[0] == "lu":
		print("\n制定服务器下用户信息查询模式")
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		serverip = data.getIp()
		data = data.getUserDetails()
		for ip, userlist in data.items():
			if ip == serverip:
				number2 = 0
				for one_user in userlist:
					number2 += 1
					print("\n  编号：" + str(number2))
					print("\n  用户："+ one_user[0])
					print("  uuid："+ one_user[1])
					print("  流量剩余："+ one_user[2])



	elif cmd[0] == "fu":
		print("\n指定用户信息查询模式")
		data = UserData()
		data.readUserData()
		data = data.getUserDetails()
		number = 0
		for ip, userlist in data.items():
			number += 1
			for one_user in userlist:
				if one_user[0] == cmd[1]:
					print("编号： "+str(number)+" 所在ip：" + ip)
					print("\n  用户："+ one_user[0])
					print("  uuid："+ one_user[1])
					print("  流量剩余："+ one_user[2])

		print("全部数据搜索完成")


	elif cmd[0] == "gvm":
		print("正在获取用户vmess")
		data = UserData()
		data.readUserData()
		data.ip = cmd[1]
		serverip = data.getIp()
		userdata = data.getUserDetails()
		uuidd = ""
		for ip, userlist in userdata.items():
			if serverip == ip:
				for one_user in userlist:
					if one_user[0] == cmd[2]:
						uuidd = one_user[1]
						vmess = getVmess(cmd[2],serverip,uuidd)
						print("\n信息码：")
						print(vmess)
		print("完成")



	elif cmd[0] == "wt":
		global state
		state = 1
		print("程序预约延迟已发送")


def mainUserUpdate():
	#一个守护进程，用于自动化更新用户的数据
	#并自动化进行移除过期用户
	while True:
		try:
			print("守护线程启动")
			
			global state
			number = 0
			while True:
				if number < 1:
					number = 60
					mainService()
				else:
					if state == 1:
						state = 0
						print("监测到主控接入，进行更新延迟 300 秒")
						time.sleep(300)
					print("守护更新进程等待：" + str(number))
					time.sleep(10)
					number -= 1

		except Exception as e:
			print(e)
			print("\n守护线程出错！")
			print("重启线程！\n")
			time.sleep(5)


def main():
	#用于给控制者提供控制端，端口的主函数
	while True:
		cmd = input(">>")
		cmd = cmd.split(" ")

		if cmd[0] == "q":
			print("\n退出程序！强制关闭所有守护进程！\n")
			sys.exit()
		elif cmd[0] == "lst":
			print("\n列出所有子进程（守护进程）\n")
			print(threading.enumerate())
		
		mainUserUpdatet = threading.Thread(target=dataControl,args=(cmd,))
		mainUserUpdatet.setDaemon(True)
		mainUserUpdatet.start()

if __name__=='__main__':
	print("Lcv2 V7.1 主服务器 启动")
	print("运行环境：Google Cloud Debian9")
	get_Lcv2_config()

	print("申请自主用户更新线程")
	mainUserUpdatet = threading.Thread(target=mainUserUpdate)
	mainUserUpdatet.setDaemon(True)
	print("线程启动！")
	mainUserUpdatet.start()

	while True:
		try:
			print("主核心启动")
			main()
		except Exception as e:
			print(e)
			print("\n核心出错！")
			print("进行全局变量初始化！")
			print("重启核心！\n")
			time.sleep(3)



		
