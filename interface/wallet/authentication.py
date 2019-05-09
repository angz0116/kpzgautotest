# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from service.gainName import getFullName
from service.districtcode import gennerator
import base64
interfaceNo = "authentication"
name = "实名认证"
import json
req = ConfigHttp()

@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 实名认证(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例,url, name, cardNo, flag, token, 预期结果):
		self.No = str(No)
		self.url = str(url)
		self.name =str(name)
		self.cardNo = str(cardNo)
		self.flag = str(flag)
		self.token = str(token)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		self.tcase = get_excel("测试用例", self.No, interfaceNo)
		print(interfaceNo + name + "CASE " + self.No)

	"""实名认证"""
	def test_body(self):
		#self.tcase
		req.httpname = "KPZG"
		self.url = get_excel("url", self.No, interfaceNo)
		#token
		self.token = get_excel("token", self.No, interfaceNo)
		# 判断是否，如果是1则从随机生成，如果是2则读取excle中，姓名，身份证号
		self.flag = get_excel("flag", self.No, interfaceNo)
		# 姓名
		self.ename = get_excel("name", self.No, interfaceNo)
		# 身份证号
		self.ecardNo = get_excel("cardNo", self.No, interfaceNo)
		if self.flag =="1":
			# 姓名
			self.name = getFullName()
			# 身份证号
			self.cardNo = gennerator()
		else:
			# excle中的姓名
			self.name = self.ename
			# excel中的身份证号
			self.cardNo = self.ecardNo
		print("实名认证，token==" + str(self.token))
		# 获取json字符串
		self.data = jsondata("wallet" + os.sep + "authentication.json")
		# base64加密，组合成字符串
		self.informatjson = {"name":self.name, "id":self.cardNo}
		# 把json转换成字符串
		self.informatstr = json.dumps(self.informatjson)
		# 再将字符串进行base64加密
		self.encodestr = base64.b64encode(self.informatstr.encode('utf-8'))
		# 最后将加密后的字符串重新赋值给information
		self.informat = str(self.encodestr,'utf-8')
		self.data["information"] = self.informat
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
			self.assertEqual(self.retcode, 0, self.logger.info("检查是否实名认证成功"))
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
		if self.flag =="1":
			set_excel(self.name, "name", self.No, interfaceNo)
			set_excel(self.cardNo,"cardNo", self.No, interfaceNo)
		set_excel(self.msg,"预期结果",self.No, interfaceNo)
	#测试后的清除工作，比如参数还原等等
	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("预期结果", self.msg)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)

if __name__ == '__main__':
	unittest.main()

