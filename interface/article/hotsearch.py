# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from datadao.sendverifysms import getSendverify
from datadao.queryverifysms import query_sql
import time
#/article/hotsearch
interfaceNo = "hotsearch"
name = "获取热门搜索 "

req = ConfigHttp()

@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 获取热门搜索(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例,url,预期结果):
		self.No = str(No)
		self.url = str(url)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		self.tcase = get_excel("测试用例", self.No, interfaceNo)
		print(interfaceNo + name + "CASE " + self.No)

	"""获取热门搜索"""
	def test_body(self):
		#self.tcase
		req.httpname = "KPZG"
		self.url = get_excel("url", self.No, interfaceNo)
		#token
		self.token = get_excel("token", self.No, "login")
		print("获取热门搜索，token==" + str(self.token))
		# 获取json字符串
		self.data = jsondata("article" + os.sep + "hotsearch.json")
		print(self.data)
		req.set_url(self.url, self.data, token=self.token)
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
			self.assertEqual(self.retcode, 0, self.logger.info("检查是否获取热门搜索成功"))
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
	#测试后的清除工作，比如参数还原等等
	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("预期结果", self.msg)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)

if __name__ == '__main__':
	unittest.main()

