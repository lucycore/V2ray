# -- coding:utf-8--
import multiprocessing
import os

from mods import install_v2,strat_v2


def strat():
	#检测是否正确安装v2ray
	if install_v2.t_v2():
		#启动程序
		strat_v2.start_v2()
	
	else:
		print("您没有安装或没有正确安装v2ray!\n")
		try:
			#删除文件的函数
			install_v2.d_v2_s()
			print("正在重新安装v2\n")
			#创建路径的函数
			install_v2.addlj()
			#安装v2的函数
			install_v2.get_v2ray()
			print("sb")
			strat()
		except:
			print("正在安装v2\n")
			#创建路径的函数
			install_v2.addlj()
			#安装v2的函数
			install_v2.get_v2ray()
			strat()

#程序入口
if __name__ == "__main__":
	#防止程序打包无限循环
	multiprocessing.freeze_support()
	print("v2ray_黑利伯瑞_内部版本\n")
	strat()
