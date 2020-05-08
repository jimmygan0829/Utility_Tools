
import random
import re
import requests
import os
import sys
rotate = {}
sticky = {}
user = ['user','123456']

with open(os.path.join(sys.path[0],"List Resi.csv")) as f:
	for idx, item in enumerate(f):
		item = item.rstrip("\n")
		temp = list(item.split(","))
		rotate[temp[0]] = temp[1]+':'+temp[2]

with open(os.path.join(sys.path[0],"Resi Smart Sticky.csv")) as f2:
	for  idx, item in enumerate(f2):
		item = item.rstrip("\n")
		temp = list(item.split(","))
		port_range = list(temp[2].split("-"))
		port_range[0]=int(re.sub(r"\s+", "", port_range[0]))
		port_range[1]=int(re.sub(r"\s+", "", port_range[1]))
		sticky[temp[0]] = [temp[1],port_range[0],port_range[1]]

while True:
	start = input("Resi Mock Gen is ready, press 1 to start, 0 to stop: ")
	while True:

		try:
			start = int(start)
			if start == 0 or start == 1:
				break
			else:
				start = input("please input 1 to start or 0 to stop: ")
		except:
			print("please input the correct input: ")
			start = input("please enter 1 to start or 0 to stop: ")


	if start == 0:
		print("program is going to halt soon, good luck on the drop")
		break
	Bot = input("please enter the bot that the proxies are intended for: ")
	Type = input("please enter the type of resi proxies you need, 0 for sticky and 1 for rotate: ")

	while True:

		try:
			Type = int(Type)
			if Type == 0 or Type == 1:
				break
			else:
				Type = input("please available type of resi proxies, 0 for sticky and 1 for rotate: ")
		except:
			#print("please input the correct input")
			Type = input("please correct type of resi proxies, 0 for sticky and 1 for rotate: ")
	output = []
	if Type == 0:
		print("The following is the regions that are available ")
		for item in list(sticky.keys()):
			print(item)
		city = input("please enter the region of the proxies (case sensitive): ")
		while True:
			if city in sticky:
				break
			else:
				city = input("please enter the region that is existed in the list, case sensitive: ")
		limit = sticky[city][2]-sticky[city][1]+1
		amount = input("please enter the amount of proxies that you need, maximum is {}: ".format(str(limit)))
		while True:
			try:
				amount = int(amount)
				if amount <=limit:
					break
				else:
					amount = input("please enter the amount that is within the limit ({}): ".format(str(limit)))
			except:
				#print("please input the correct input: ")
				amount = input("please correct input, within the limit ({}): ".format(str(limit)))
		user[0] = input("please enter your username: ")
		user[1] = input("please enter the pw: ")
		port_list = random.sample(range(sticky[city][1],sticky[city][2]+1),amount)
		for num in port_list:

			temp_item = sticky[city][0]+":"+str(num)+":"+user[0]+":"+user[1]
			
			output.append(temp_item+"\n")

	else:

		print("The following is the regions that are available ")
		for item in list(rotate.keys()):
			print(item)
		city = input("please enter the region of the proxies (case sensitive): ")
		while True:
			if city in rotate:
				break
			else:
				city = input("please enter the region that is existed in the list, case sensitive: ")
		user[0] = input("please enter your username: ")
		user[1] = input("please enter the pw: ")
		output.append(rotate[city]+":"+user[0]+":"+user[1])

	o = open(os.path.join(sys.path[0],"{}.txt".format(Bot)),"w")
	o.truncate(0)
	for idx,i in enumerate(output):
		o.write(output[idx])
	o.close()






