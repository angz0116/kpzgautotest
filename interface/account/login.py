# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest

interfaceNo = "login"
name = "用户登录"

req = ConfigHttp()

@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 用户登录(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例,url, mobile, password, uid, countrycode, token, 预期结果):
		self.No = str(No)
		self.url = str(url)
		self.mobile = str(mobile)
		self.password = str(password)
		self.uid = str(uid)
		self.countrycode =str(countrycode)
		self.token = str(token)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		self.tcase = get_excel("测试用例", self.No, interfaceNo)
		print(interfaceNo + name + "CASE " + self.No)

	"""用户登录"""
	def test_body(self):
		#self.tcase
		req.httpname = "KPZG"
		self.url = get_excel("url", self.No, interfaceNo)
		# 手机号
		self.mobile = get_excel("mobile", self.No, interfaceNo)
		# 国家编码
		self.countrycode = get_excel("countrycode", self.No, interfaceNo)
		# 密码
		self.password = get_excel("password", self.No, interfaceNo)
		print("用户登录接口__login手机号==" + str(self.mobile))
		# 获取json字符串
		self.data = jsondata("account" + os.sep + "login.json")
		# 动态获取手机号
		self.data["mobile"] = self.mobile
		# 动态获取密码
		self.data["password"] = self.password
		# 国家编码
		self.data["country_code"] = self.countrycode
		print(self.data)
		req.set_url(self.url, self.data, token="")
		req.set_data(self.data)
		self.response = req.post()
		try:
			if self.response is None:
				self.retcode = 1
				self.msg = "报文返回为空！"
			else:
				print(self.response)
				self.retcode = self.response["code"]
				self.msg = self.response["msg"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")
		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, 0, self.logger.info("检查是否登录成功"))
			if self.retcode==0:
				if "data" in self.response:
					self.tokenp = self.response["data"]["token"]
					self.uid = self.response["data"]["uid"]
					set_excel(self.tokenp, "token", self.No, interfaceNo)
					set_excel(self.uid, "uid", self.No, interfaceNo)
					set_excel(self.tokenp, "token", self.No, "authentication")

			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError as ae:
			print("实际结果与预期结果：")
			print(ae)
			self.logger.info("实际结果与预期结果：")
			self.logger.error(ae)
			set_excel("fail", "测试结果", self.No, interfaceNo)
			self.logger.error("测试失败")
		self.logger.info(self.msg)
	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.msg,"预期结果",self.No, interfaceNo)
		set_excel(self.password, "password", self.No, interfaceNo)
		set_excel(self.mobile,"mobile", self.No, interfaceNo)
		
	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("预期结果", self.msg)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)

if __name__ == '__main__':
	unittest.main()

