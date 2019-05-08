# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from service.gainName import getFullName

interfaceNo = "sciupdate"
name = "科普员信息修改"

req = ConfigHttp()

@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 科普员信息修改(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例,url, province, provincecode, city, citycode, county, countycode, town, towncode, companyname, protocol, name, sciencetype, 预期结果):
		self.No = str(No)
		self.url = str(url)
		self.province = str(province)
		self.provincecode = str(provincecode)
		self.city = str(city)
		self.citycode = str(citycode)
		self.county = str(county)
		self.countycode = str(countycode)
		self.town = str(town)
		self.towncode = str(towncode)
		self.companyname = str(companyname)
		self.protocol = str(protocol)
		self.name = str(name)
		self.sciencetype = str(sciencetype)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		self.tcase = get_excel("测试用例", self.No, interfaceNo)
		print(interfaceNo + name + "CASE " + self.No)

	"""科普员信息修改"""
	def test_body(self):
		#self.tcase
		req.httpname = "KPZG"
		self.url = get_excel("url", self.No, interfaceNo)
		#token
		self.token = get_excel("token", self.No, "login")
		print("科普员信息修改，token==" + str(self.token))
		# 省会编码
		self.provincecode = get_excel("provincecode", self.No, interfaceNo)
		# 省会名称
		self.province = get_excel("province", self.No, interfaceNo)
		# 城市编码
		self.citycode = get_excel("citycode", self.No, interfaceNo)
		# 城市名称
		self.city = get_excel("city", self.No, interfaceNo)
		# 市区编码
		self.countycode = get_excel("countycode", self.No, interfaceNo)
		# 市区街道编码
		self.county = get_excel("county", self.No, interfaceNo)
		# 市区街道编码
		self.towncode = get_excel("towncode", self.No, interfaceNo)
		# 市区街道名称
		self.town = get_excel("town", self.No, interfaceNo)
		# 单位名称
		self.companyname = get_excel("companyname", self.No, interfaceNo)
		# 是否勾选认证复选框
		self.protocol = get_excel("protocol", self.No, interfaceNo)
		# 姓名
		self.name = getFullName()
		# 科普人员类型
		self.sciencetype = get_excel("sciencetype", self.No, interfaceNo)
		print("科普员修改接口，token==" + str(self.token))
		# 获取json字符串
		self.data = jsondata("sciencer" + os.sep + "sciupdate.json")
		self.data["name"] = self.name
		self.data["province_code"] = self.provincecode
		self.data["province"] = self.province
		self.data["city_code"] = self.citycode
		self.data["city"] = self.city
		self.data["county_code"] = self.countycode
		self.data["county"] = self.county
		self.data["town_code"] = self.towncode
		self.data["town"] = self.town
		self.data["companyname"] = self.companyname
		self.data["protocol"] = self.protocol
		self.data["science_type"] = self.sciencetype
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
			self.assertEqual(self.retcode, 0, self.logger.info("检查是否科普员信息修改成功"))
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

