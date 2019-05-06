# -*- coding:utf-8 -*-
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import threading
import utils.readConfig as readConfig
from utils.baseLog import MyLog
import zipfile
import glob

Config = readConfig.ReadConfig()

class Email():
	def __init__(self):
		global host, user, password, port, sender, title, content
		host = Config.get_email("mail_host")
		user = Config.get_email("mail_user")
		password = Config.get_email("mail_pass")
		port = Config.get_email("mail_port")
		sender = Config.get_email("sender")
		title = Config.get_email("subject")
		content = Config.get_email("content")
		self.value = Config.get_email("receiver")
		self.receiver = []
		if len(self.value)>0:
			for n in str(self.value).split(";"):
				self.receiver.append(n)
		else:
			self.logger.info("收件人不能为空")
		date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.subject = title + " " + date
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.msg = MIMEMultipart('mixed') #related,alternative

	def config_header(self):
		# 邮件主题
		self.msg['subject'] = self.subject
		# 发送者账号
		self.msg['from'] = sender
		# 接收者账号列表
		self.msg['to'] = ",".join(self.receiver)

	def config_content(self):
		# content_plain = MIMEText(content, 'plain', 'utf-8')
		# self.msg.attach(content_plain)
		# 保存图片的path
		self.imgpath = self.log.get_img_path()
		# 填写邮件内容，html超文本
		mail_msg = '''
				<p>\n\t ''' + content + '''</p>
				<p>测试结果如下图：</p>
				<p><img src="cid:image1"></p>
				'''
		self.msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))
		try:
			# 指定图片为当前目录
			self.imgfile = open(self.imgpath, 'rb')
			self.msgImage = MIMEImage(self.imgfile.read())
			self.imgfile.close()
			# 定义图片 ID，在 HTML 文本中引用
			self.msgImage.add_header('Content-ID', '<image1>')
			self.msg.attach(self.msgImage)
		except FileExistsError as ex:
			print("********未获取到截图信息********")
			self.logger.info("********未获取到截图信息********")

	def config_file(self):
		# 获取log日志的邮件路径
		resultpath = self.log.get_result_path()
		# 处理带附件的情况
		if self.check_file():
			files = glob.glob(resultpath + '/*')
			#添加附件1
			with open(files[1], 'rb') as reportfile:
				filehtml = MIMEText(reportfile.read(), 'base64', 'utf-8')
				filehtml.add_header('Content-Disposition', 'attachment', filename="测试报告.html")
				filehtml.add_header('Content-ID', '<0>')
				filehtml.add_header('X-Attachment-Id', '0')
				filehtml.add_header('Content-Type', 'application/octet-stream')
				self.msg.attach(filehtml)
			#添加附件2
			with open(files[0], 'rb') as logfile:
				filelog = MIMEText(logfile.read(), 'base64', 'utf-8')
				filelog.add_header('Content-Disposition', 'attachment', filename="测试日志.txt")
				filelog.add_header('Content-ID', '<0>')
				filelog.add_header('X-Attachment-Id', '0')
				filelog.add_header('Content-Type', 'application/octet-stream')
				self.msg.attach(filelog)

	def check_file(self):
		reportpath = self.log.get_report_path()
		if os.path.isfile(reportpath) and not os.stat(reportpath) == 0:
			return True
		else:
			return False

	'''
	发送邮件函数
	:param mail_host: 邮箱服务器
	:param port: 端口号
	:param username: 邮箱账号 
	:param passwd: 邮箱密码(不是邮箱的登录密码，是邮箱的授权码)
	:param recv: 邮箱接收人地址，多个账号以逗号隔开
	:param title: 邮件标题
	:param content: 邮件内容
	:return:
	'''
	def send_email(self):
		self.config_header()
		self.config_content()
		self.config_file()
		try:
			# 如果发送者是qq邮箱，则用ssl
			if sender.endswith("qq.com"):
				smtp = smtplib.SMTP_SSL(host,port)
			else:
				smtp = smtplib.SMTP(host,port)
			# 发送邮件服务器对象
			smtp.login(user, password)
			smtp.sendmail(sender, self.receiver, self.msg.as_string())
			smtp.quit()
			print("测试报告已发送邮件!!!")
			self.logger.info("测试报告已发送邮件")
		except Exception as ex:
			self.logger.error(str(ex))
			print("测试报告发送邮件失败!!!")
			self.logger.info("测试报告发送邮件失败")
class MyEmail():
	email = None
	mutex = threading.Lock()

	def __init__(self):
		pass

	@staticmethod
	def get_email():

		if MyEmail.email is None:
			MyEmail.mutex.acquire()
			MyEmail.email = Email()
			MyEmail.mutex.release()
		return MyEmail.email


