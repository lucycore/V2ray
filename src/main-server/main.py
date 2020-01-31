# -- coding:utf-8--
#this file set in the main server
import socket
import time
import datetime
import json
import os
import uuid

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
		except:
			print("\n\nUserData类内部错误！！")
			print("读取用户数据库失败！\n\n")


	def writeUserData(self):
		try:
			with open(self.path,'w') as ojbk:
				json.dump(self.userdata,ojbk)
		except:
			print("\n\nUserData类内部错误！！")
			print("写入用户数据库失败！\n\n")


	def addUser(self):
		try:
			one_user_data_list = [self.email,self.uuid,self.traffic]
			self.userdata[self.ip].append(one_user_data_list)
		except:
			print("\n\nUserData类内部错误！！")
			print("添加用户到指定的ip下失败！\n\n")


	def delUser(self):
		sonserver_users = self.userdata[self.ip]
		
		user_index = 0
		find_state = False
		for one_user_data in sonserver_users:
			if one_user_data[0] == self.email:
				find_state = True
				break
			else:
				user_index += 1

		if find_state :
			del self.userdata[self.ip][user_index]

		else:
			print("\n\nUserData类内部错误！！")
			print("在用户数据库之中没有找到要删除的用户！\n\n")


	def addServer(self):
		try:
			self.userdata[self.ip] = []
		except:
			print("\n\nUserData类内部错误！！")
			print("添加服务器到用户数据库失败！\n\n")


	def delServer(self):
		try:
			del self.userdata[self.ip]
		except:
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
			if state == False:
				print("\n\nUserData类内部错误！！")
				print("没有找到要添加流量的用户！\n\n")

		except:
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

			if state == False:
				print("\n\nUserData类内部错误！！")
				print("没有找到要删除流量的用户！\n\n")

		except:
			print("\n\nUserData类内部错误！！")
			print("删除流量到用户出错！\n\n")



	def getUserDetails(self):
		try:
			return self.userdata
		except:
			print("\n\nUserData类内部错误！！")
			print("返回用户信息细节失败！\n\n")


class Lcv2_Socket():

	def __init__(self,ip="",email="",uuid=""):
		self.ip = ip
		self.email = email
		self.uuid = uuid
		self.sock = socket.socket()


	def connectServer(self):
		HOST = self.ip
		PORT = 2233
		self.sock.connect((HOST, PORT))
		

	def addLcv2User(self):
		#用于添加用户的函数

		dataList = ["add_user",self.email,self.uuid]
		data = '*data*'.join(dataList)

		self.sock.sendall(data.encode())
		serverRecv = self.sock.recv(1024).decode()

		if serverRecv == "True":
			return True
		else:
			return False


	def delLcv2User(self):
		#用于删除用户的函数
		
		dataList = ["del_user",self.email,self.uuid]
		data = '*data*'.join(dataList)

		self.sock.sendall(data.encode())
		serverRecv = self.sock.recv(1024).decode()

		if serverRecv == "True":
			return True
		else:
			return False


	def readLcv2User(self):
		#用于读取用户流量使用情况的函数

		dataList = ["read_user",self.email]
		data = '*data*'.join(dataList)

		self.sock.sendall(data.encode())
		serverRecv = self.sock.recv(1024).decode()

		try:
			serverRecv = int(serverRecv)
			return True, serverRecv
		except:

			return False, 0


	def closeConnect(self):
		self.sock.close()


def mainService():
	#用于服务器自动化删除流量耗尽用户
	print("流量消耗更新服务开启")

	data = UserData()
	data.readUserData()
	userdata = data.getUserDetails()
	
	lcv2Sock = Lcv2_Socket()

	for server_ip, users in userdata.items():
		for one_user in users:
			print("\n查找用户：" + one_user[0])
			lcv2Sock.ip = server_ip
			lcv2Sock.email = one_user[0]
			lcv2Sock.connectServer()
			state, traffic = lcv2Sock.readLcv2User()

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
				lcv2Sock.delLcv2User()
				lcv2Sock.closeConnect()

	data.writeUserData()
	print("清除行为完成！")


def dataControl():

	print("\n\nLcv2 用户信息主控模块启动\n")

	while True:
		cmd = input(">>")
		cmd = cmd.split(" ")

		if cmd[0] == "h":
			print("\nLcv2 信息主控使用帮助（自动保存）")
			print("au [ip] [email] [traffic] 添加用户到服务器下")
			print("du [ip] [email] [uuid] 删除用户在服务器下")
			print("at [ip] [email] [traffic] 添加用户流量")
			print("dt [ip] [email] [traffic] 删除用户流量")
			print("initserver 进行服务器初始化")
			print("ud 更新用户流量数据 ")
			print("as [ip] 添加服务器")
			print("ds [ip] 删除服务器\n")
			print("---------信息查找浏览分类---------")
			print("la 列出所有用户信息")
			print("ls 列出所有服务器信息")
			print("lu [ip] 列出指定ip下的所有用户")
			print("fu [email] 查询指定用户在所有ip下")



		elif cmd[0] == "au":
			print("添加用户模式")
			uuidd = str(uuid.uuid4())
			data = UserData()
			data.readUserData()
			data.ip = cmd[1]
			data.email = cmd[2]
			data.uuid = uuidd
			data.traffic = cmd[3]
			data.addUser()
			data.writeUserData()

			sock = Lcv2_Socket()
			sock.ip = cmd[1]
			sock.email = cmd[2]
			sock.uuid = uuidd
			sock.connectServer()
			sock.addLcv2User()
			sock.closeConnect()
			print("完成")

		elif cmd[0] == "du":
			print("删除用户模式")
			data = UserData()
			data.readUserData()
			data.ip = cmd[1]
			data.email = cmd[2]
			data.uuid = cmd[3]
			data.delUser()
			data.writeUserData()

			sock = Lcv2_Socket()
			sock.ip = cmd[1]
			sock.email = cmd[2]
			sock.uuid = cmd[3]
			sock.connectServer()
			sock.delLcv2User()
			sock.closeConnect()
			print("完成")

		elif cmd[0] == "at":
			print("添加用户流量模式")
			data = UserData()
			data.readUserData()
			data.ip = cmd[1]
			data.email = cmd[2]
			data.traffic = cmd[3]
			data.addTraffic()
			data.writeUserData()
			print("完成")

		elif cmd[0] == "dt":
			print("删除用户流量模式")
			data = UserData()
			data.readUserData()
			data.ip = cmd[1]
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
			data.delServer()
			data.writeUserData()

		elif cmd[0] == "la":
			print("\n全部用户信息查询模式")
			data = UserData()
			data.readUserData()
			data = data.getUserDetails()
			for ip, userlist in data.items():
				print("\n服务器ip：" + ip)
				for one_user in userlist:
					print("\n  用户："+ one_user[0])
					print("  uuid："+ one_user[1])
					print("  流量剩余："+ one_user[2])

		elif cmd[0] == "ls":
			print("\n服务器信息查询模式\n")
			data = UserData()
			data.readUserData()
			data = data.getUserDetails()
			for ip, userlist in data.items():
				print("服务器ip：" + ip)
				

		elif cmd[0] == "lu":
			print("\n制定服务器下用户信息查询模式")
			data = UserData()
			data.readUserData()
			data = data.getUserDetails()
			for ip, userlist in data.items():
				if ip == cmd[1]:
					for one_user in userlist:
						print("\n  用户："+ one_user[0])
						print("  uuid："+ one_user[1])
						print("  流量剩余："+ one_user[2])
				else:
					print("错误！没有找到服务器")


		elif cmd[0] == "fu":
			print("\n指定用户信息查询模式")
			data = UserData()
			data.readUserData()
			data = data.getUserDetails()
			for ip, userlist in data.items():
				for one_user in userlist:
					if one_user[0] == cmd[1]:
						print("所在ip：" + ip)
						print("\n  用户："+ one_user[0])
						print("  uuid："+ one_user[1])
						print("  流量剩余："+ one_user[2])

			print("全部数据搜索完成")


dataControl()





		