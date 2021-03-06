# -*- coding:utf-8 -*-

import os
import unittest
from utils.baseLog import MyLog as Log
import utils.readConfig as readConfig
from utils.HTMLTestReport import HTMLTestRunner
from utils.baseEmail import MyEmail
from service.gainHtml import savescreenimg

Config = readConfig.ReadConfig()
class mytestRun:
	def __init__(self):
		"""
		初始化需要的参数
		:return：
		"""
		global log, logger, resultPath, on_off
		# log初始化
		log = Log.get_log()
		logger = log.logger
		# 定义结果保存路径
		resultPath = log.get_report_path()
		on_off = Config.get_email("on_off")
		#logger.info("发送邮件已打开，状态为"+on_off)
		# 取得config\caselist.txt文件路径
		self.caseListFile = os.path.join(readConfig.proDir, "config", "caselist.txt")
		# 取得test_case文件路径
		self.caseFile = os.path.join(readConfig.proDir, "interface")
		# 定义一个空里列表，用于保存类名
		self.caseList = []
		self.email = MyEmail.get_email()

	def set_case_list(self):
		with open(self.caseListFile, encoding="utf-8") as fb:
			for value in fb.readlines():
				data = str(value)
				if data != '' and not data.startswith("#"):
					self.caseList.append(data.replace("\n", ""))


	def set_case_suite(self):
		self.set_case_list()
		test_suite = unittest.TestSuite()
		suite_module = []

		for case in self.caseList:
			discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case + '.py', top_level_dir=None)
			suite_module.append(discover)
		if len(suite_module) > 0:
			for suite in suite_module:
				for test_name in suite:
					test_suite.addTest(test_name)
		else:
			return None
		return test_suite

	def runAll(self):
		try:
			suit = self.set_case_suite()
			if suit is not None:
				print("********TEST START********")
				logger.info("********TEST START********")
				with open(resultPath, 'wb') as fp:
					runner = HTMLTestRunner(stream=fp, title='科普中国APP接口测试报告', description='详细测试用例结果', tester='赵爱')
					runner.run(suit)
					# 把测试报告截图生成保存到log日志，report.html测试报告同一文件夹
					savescreenimg(resultPath)
			else:
				logger.info("没有添加一个用例")
		except Exception as ex:
			logger.error(str(ex))
		finally:
			print("*********TEST END*********")
			print("*********发送邮件 START*********")
			logger.info("*********TEST END*********")
			logger.info("*********发送邮件 START*********")
			if on_off == "on":
				self.email.send_email()
			elif on_off == 'off':
				logger.info("不能发送邮件，因为on_off = 'off'")
			else:
				logger.info("无状态.")
			print("*********发送邮件 END*********")
			logger.info("*********发送邮件 END*********")
if __name__ == '__main__':
	obj = mytestRun()
	obj.runAll()


