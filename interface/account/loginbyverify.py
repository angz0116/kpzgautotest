# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from datadao.sendverifysms import getSendverify
from datadao.queryverifysms import query_sql
import time

interfaceNo = "loginbyverify"
name = "手机号快捷登录"

req = ConfigHttp()

@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 手机号快捷登录(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例,url, mobile, verify, flag, uid, countrycode, token, 预期结果):
		self.No = str(No)
		self.url = str(url)
		self.mobile = str(mobile)
		self.verify = str(verify)
		self.flag = str(flag)
		self.uid = str(uid)
		self.countrycode =str(countrycode)
		self.token = str(token)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		self.tcase = get_excel("测试用例", self.No, interfaceNo)
		print(interfaceNo + name + "CASE " + self.No)

	"""手机号快捷登录"""
	def test_body(self):
		#self.tcase
		req.httpname = "KPZG"
		self.url = get_excel("url", self.No, interfaceNo)
		# 手机号
		self.mobile = get_excel("mobile", self.No, interfaceNo)
		# 国家编码
		self.countrycode = get_excel("countrycode", self.No, interfaceNo)
		#根据flag为1时，已存在验证码，不为1时，重新生成新的验证码
		self.flag = get_excel("flag", self.No, interfaceNo)
		if self.flag == "1":
			self.verifycode = get_excel("verify", self.No, interfaceNo)
		else:
			# 获取验证码的方法
			self.veresult = getSendverify(self.logger, "4", self.mobile, self.countrycode)
			if self.veresult == 0:
				time.sleep(10)
				# 从数据库中查询验证码
				self.verifycode = query_sql(self.logger, self.mobile, self.countrycode)
		
		print("手机号快捷登录接口__login手机号==" + str(self.mobile))
		# 获取json字符串
		self.data = jsondata("account" + os.sep + "loginbyverify.json")
		# 动态获取手机号
		self.data["mobile"] = self.mobile
		# 动态获取密码
		self.data["verify"] = self.verifycode
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
	# 断言检查结果
	def check_result(self):
		try:
			self.assertEqual(self.retcode, 0, self.logger.info("检查是否手机号快捷登录成功"))
			if self.retcode==0:
				if "data" in self.response:
					self.tokenp = self.response["data"]["token"]
					self.uid = self.response["data"]["uid"]
					set_excel(self.tokenp, "token", self.No, interfaceNo)
					set_excel(self.uid, "uid", self.No, interfaceNo)

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
		set_excel(self.verify, "verify", self.No, interfaceNo)
		set_excel(self.mobile,"mobile", self.No, interfaceNo)
	#测试后的清除工作，比如参数还原等等
	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("预期结果", self.msg)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)

if __name__ == '__main__':
	unittest.main()

