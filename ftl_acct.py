import requests
from random import randint,sample
import sys,os
from bs4 import BeautifulSoup
import smtplib
import time
import imaplib
import email
#url = 'https://www.footlocker.co.uk/INTERSHOP/web/FLE/Footlocker-Footlocker_GB-Site/en_GB/-/GBP/ViewUserAccountActivation-ActivateAccount?Login=jimmydagreatchef2%40gmail.com&Hash=3a8a3661-9acc-4165-96de-2c52cc9b98cd'

head = {
  'authority': 'www.footlocker.co.uk',
  'upgrade-insecure-requests': '1' ,
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'dnt': '1',
  'sec-fetch-site': 'none', 
  'sec-fetch-mode': 'navigate' ,
  'sec-fetch-dest': 'document',
  'accept-language' : 'en'
 }

# 3. footlocker eu账号激活器

# 跑过大象的都知道，之前yeezy 350有一次发售，需要强制账号才能加车
# 用大象注册时，会给你的邮箱发送一封 verify 邮件
# 本项目要求:

# - 输入为一个verify邮件中的激活链接的列表（提取方式有很多，可以读取你的email，也可以通过页面的正则等)
# - 自行研究ftl eu的账号激活流程
# - 利用程序实现，并将激活的结果进行输出

# hint:
# - ftl eu的激活就是对链接进行访问，但需要带上一些headers等信息，否则会失败
# - 成功与否需要对返回的html进行解析，具体字段请自行实验

# ORG_EMAIL   = "@gmail.com"
# FROM_EMAIL  = "jimmydagreatchef2" + ORG_EMAIL
# FROM_PWD    = "814582160Jy"
# SMTP_SERVER = "imap.gmail.com"
# SMTP_PORT   = 993


# def read_email_from_gmail():
#     # try:
#     mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#     mail.login(FROM_EMAIL,FROM_PWD)
#     mail.select('inbox')
#     type,data = mail.search(None, 'ALL')
#     mail_ids = data[0]
#     #****
#     stuff = data[0].decode('UTF-8')
#     #print(stuff)
#     data_list = stuff.split(" ")
#     #print("\n") 
#     #print(data_list)
    
#     #******
#     id_list = data_list#mail_ids.split()   
#     first_email_id = int(id_list[0])
#     latest_email_id = int(id_list[-1]) 
#     i = latest_email_id
#     while i>=740:
#         typ, data = mail.fetch(str(i), '(RFC822)' )
#         #print(data)
#         for response_part in data:
#             if isinstance(response_part, tuple):
#                 msg = email.message_from_string(response_part[1].decode('UTF-8'))
#                 email_subject = msg['subject']
#                 email_from = msg['from']
#                 print ('From : ' + email_from + '\n')
#                 print ('Subject : ' + email_subject + '\n')

#         i = i - 1
    

def checking( content ):
	sample = 'Success! Welcome to Foot Locker'
	try:
		soup = BeautifulSoup(content, 'html.parser')
		status = soup.find_all('h2',{"class": "fl-error-and-password-page--headline"})
		
		for item in status:
			#print(item.get_text(),type(item.get_text()))
			if sample in item.get_text():
				print("Account Activated")
				return True
		print("Account activation Failed, please check your link")
		return False
	except:
		print("Account activation Failed, please check your link")
		return False



start = input("Press 1 to start the program ")
while True:
	try:
		start = int(start)
		if start == 1:
			break
	except:
		start = input("Invalid input, please press 1 to start the program")

while start == 1:

	input_source = input("enter the activation link for the account please: ")
	try:
		response = requests.get(input_source,headers = head)
		if response.status_code != 200:
			print("Please check your link or your proxy connection, as a connection error occured: Error {}".format(response))
			continue
		checking(response.text)
	except:
		print("Unexpected Errors occured during activation process, please check your link")
		continue

	print("Press Ctrl+C to HALT the program, if you want to stop.")
	


