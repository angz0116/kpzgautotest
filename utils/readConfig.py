# -*- coding:utf-8 -*-

import os ,sys
import codecs
import configparser

# 获取当前文件路径
proDir = os.path.dirname(os.path.dirname(__file__))
configPath = os.path.join(proDir, "config", "config.ini")
class ReadConfig:
	def __init__(self):
		with open(configPath, 'rb') as fd:
			data = fd.read()
			if data[:3] == codecs.BOM_UTF8:
				data = data[3:]
				with codecs.open(configPath, "w") as file:
					file.write(data)

		self.cf = configparser.ConfigParser()
		self.cf.read(configPath, encoding="utf-8-sig")

	#获取邮箱
	def get_email(self, name):
		value = self.cf.get("EMAIL", name)
		return value
	#获取http连接
	def get_http(self, http, name):
		value = self.cf.get(http, name)
		return value
	#获取数据库连接
	def get_db(self, db, name):
		value = self.cf.get(db, name)
		return value

