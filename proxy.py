
import sys
import os
import time
import requests
testing_site = input("please enter the site you want to test on: ")
filter_ping = input("please enter desired ping for output proxies in ms: ")
filter_ping = float(filter_ping)
output = []
with open(os.path.join(sys.path[0],"input_proxy/input.txt")) as f:
	# read_l = f.readline()
	# count = 1
	# print(read_l, type(read_l))
	# while read_l:
	# 	print('line {} is {}'.format(count, read_l))
	# 	read_l = f.readline()
	# 	count +=1
	for idx, line in enumerate(f):
		#print('line {} is {}'.format(idx+1, line))
		single_proxy =line.split(':')
		user_info = single_proxy[2]+':'+single_proxy[3].rstrip("\n")
		
		proxy_w_port = single_proxy[0]+':'+single_proxy[1]
		proxies = {}
		proxies['http']='http://'+user_info+'@'+proxy_w_port+'/'
		proxies['https'] = 'http://'+user_info+'@'+proxy_w_port+'/'
		#print(proxies)
		ping = []
		bad = 0
		for i in range(5):
			start = time.time()
			#print(proxies,'this is the proxies after we clean input ')
			try:
				res = requests.get(testing_site,proxies = proxies,timeout = 3)
			#print

				if res:
					ping_time = time.time()-start
					#print(ping_time,'testing')
					ping.append(ping_time)
					#print(res)
			except:
				bad = 1
				
				continue
		if bad == 0 :
			tot = sum(ping) ##
			avg_ping = tot/5
			
			print('{} ping: {}'.format(line.rstrip("\n"), int(avg_ping*1000)))
			if avg_ping <=filter_ping/1000:
				output.append(line)

		else:
			print('{} bad  proxies'.format(line.rstrip("\n")))
			bad = 0
			#print('{} is bad proxies'.format(line))


	#print(output)
o = open("output.txt","w")
o.truncate(0)
for idx,i in enumerate(output):
	o.write(output[idx])
o.close()





		