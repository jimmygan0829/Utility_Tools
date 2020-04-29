from discord import Webhook, RequestsWebhookAdapter, Embed, Colour
import datetime
import time
from discord.ext import commands
import requests
import json
import jsonpath
#import keyboard


# def restock_monitor (new_item):
#     foo = request.get('https://packershoes.com/products.json')
#     if new_item == 0:

# this it the monitor for packer shoes

def monitor_link_packer( link,sizing_info_map,monitor_map):
    send_command = 0 #default send command to be 0
    # input section would be modified for discord interaction
    while link[:8].lower() != 'https://':                       
        link = input('please input a  correct format of prodcut link and include the https://')
    if site_select == 1:
        list_link = link.split('?')
        filtered_link = list_link[0] + '.json'
        product_link = filtered_link

    foo = requests.get(product_link)
    if foo.text == '':
        return False
    try:
        f2 = json.loads(foo.text)
    except:
        return False
    title = jsonpath.jsonpath(f2,"$.product.title")[0]
    if title == False:
        return False
    image_extract = jsonpath.jsonpath(f2,"$.product.image")[0]
    if image_extract == False:
        return False
    thumbnail = image_extract['src']
    site = 'https://packershoes.com/'
    price = ''
    output_info_dict = {'product':title,'product-link':link,'site':site,'thumbnail':thumbnail}
    product_all = jsonpath.jsonpath(f2,"$.product.variants")[0]
    if product_all == False:
        return False
    atc1 = []
    atc2 = []
 
    for idx, product in enumerate(product_all):   
        if price == '':
            price = product['price']+' USD'
    
        atc = 'https://packershoes.com/cart/'+str(product['id'])+':1'
        if product['sku'] not in sizing_info_map or product['sku'] not in monitor_map:
             # initial instance 
            send_command = 1
            sizing_info_map[product['sku']] = [product['option1'],atc]
            monitor_map[product['sku']] =  product['inventory_quantity']
        else:
            # the following update
            if monitor_map[product['sku']]-product['inventory_quantity']!=0: #stock update is true, so send webhook
                send_command = 1
                monitor_map[product['sku']] = product['inventory_quantity']
        item = product['sku']
        if idx %2 == 0: # current items in the map ready to pack and send
            if monitor_map[item] != 0:
                single_field = sizing_info_map[item]
                single_field.append(str(monitor_map[item]))

                atc1.append(tuple(single_field))
        else:
            if monitor_map[item] != 0:
                single_field = sizing_info_map[item]
                single_field.append(str(monitor_map[item]))
                atc2.append(tuple(single_field))
    
    
    total_stock = sum(monitor_map.values())
    output_fields = {"price": price,"stock" :str(total_stock)}
    
    output_fields["atc1"] = atc1
    output_fields["atc2"] = atc2
    if send_command == 1:
        if webhook_format == 1:
            Cyber_webhook(user_name= author_name, avi_url=author_icon_url,webhook_link=webhook_url,info_dic=output_info_dict,fields= output_fields,custom = customize)
        if webhook_format == 2:
            Balko_webhook(user_name= author_name, avi_url=author_icon_url,webhook_link=webhook_url,info_dic=output_info_dict,fields= output_fields,custom = customize)
        if webhook_format == 3:
            TKS_webhook(user_name= author_name, avi_url=author_icon_url,webhook_link=webhook_url,info_dic=output_info_dict,fields= output_fields,custom = customize)
    
    return True




# 2. 简单shopify 监控器

# - 支持如undefeated网站的单品尺码监控，即当监控的单品更新尺码时，发送提醒到自定义的webhook
# - 支持自定义webhook
# - 做好错误处理，需要能够长期运行
# - 附加题 实现undfeated的上新监控





sample_fields = {"price":"800USD","stock":"120","atc1":[("8","https://www.google.com","2"),("9","https://www.google.com","4")],"atc2":[]}
sample_info_dict = {'product':"stuff I always want",'product-link':"https://www.google.com",'site':"https://www.google.com",'thumbnail':"https://pbs.twimg.com/media/EJl-vwIWoAAgIAo.jpg"}


mode = input("please input your selected mode, 1 for manual, 0 for monitor: ") 			# default for monitor mode 0, 1 is for manual mode
mode = int(mode)
webhook_format = input("please input your selected webhook format, 1 for Cyber, 2 for Balko, and 3 for TKS: ")
webhook_format = int(webhook_format)
webhook_url = input("please input your webhook url: ")
customize = input("please indicate if you want to customize your profile pic and author name, 1 for YES and 0 for NO: ")
customize = int(customize)
author_name = input("input your preferred name [Skip if you put 0 in customize]: ")
author_icon_url = input("please paste the link of the picture to be your profile avi [Skip if you put 0 in customize]: ")
if customize ==1 and "https://" not in author_icon_url[:8]:
    author_icon_url = input("please re-enter your link of the picture, and make sure include https://")



def send_error_msg(content,url_error):
    url = url_error
    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
    embed = Embed()
    embed.add_field(name="Error", value="{}".format(content)).set_footer(text="Error_Detector")
    webhook.send('Monitor will be stopped please restart the monitor', embed=embed)



def datetime_cyberize(now):
	now_l = now.split('-')
	rest = now_l[2].split(' ')
	day = rest[0]
	new_date = day+'/'+now_l[1]+'/'+now_l[0]
	time = rest[-1]
	new_stamp =  new_date+' '+time[:-3]
	return new_stamp


#fields{price:,stock:,atc1:[("size", "atc link","stock"),...],atc2:}
def TKS_webhook(user_name, avi_url, webhook_link, info_dic, fields, custom): #info_dict{product link, title, site, thumbnail,} 
    if custom == 0:
        user_name = "TheKickStation"
        avi_url = "https://pbs.twimg.com/profile_images/1011541359382052866/4Ewy9XIw_400x400.jpg"

    webhook = Webhook.from_url(webhook_link, adapter=RequestsWebhookAdapter())
    embed = Embed(title=info_dic['product'],colour=0x6651a2,url=info_dic['product-link'])
    
    footer = user_name
    embed.set_footer(text=footer,icon_url = avi_url)
    embed.set_author(name=info_dic['site'],url = info_dic['site'])
    embed.set_thumbnail(url = info_dic['thumbnail'])
    embed.add_field(name="Price",value = fields["price"])
    embed.add_field(name="Stock",value = fields["stock"])
    atc1_value = ""
    if len(fields["atc1"]) >0:
        for i in range(len(fields["atc1"])):
            
            atc1_value +=  "["+fields["atc1"][i][0]+"]("+fields["atc1"][i][1]+") | "+fields["atc1"][i][2]+"\n"
            
    else:
        atc1_value = '\u200b'

    atc2_value = ""
    
    if len(fields["atc2"]) >0:
        for i in range(len(fields["atc2"])):
            
            atc2_value += "["+fields["atc2"][i][0]+"]("+fields["atc2"][i][1]+") | "+fields["atc2"][i][2]+"\n"
           
    else:
        atc2_value = '\u200b'

    embed.add_field(name="ATC", value = atc1_value)
    embed.add_field(name="ATC", value = atc2_value)
    datetime_list = str(datetime.datetime.now()).split(".")
    datetime_now = datetime_list[0]

    embed.add_field(name="Time stamp (utc)", value = datetime_now)

    user = info_dic['site'] # only support https://youtube.com/ with / at the end
    user = user[8:]
    if "www." == user[:4]:
        user = user[4:]
    if "/" == user[-1]:
        user = user[:-1]

    
    webhook.send("",embed=embed,username = user,avatar_url=avi_url)

#fields{price:,stock:,atc1:[("size", "atc link","stock"),...],atc2:}
def Balko_webhook(user_name, avi_url, webhook_link, info_dic, fields,custom): #info_dict{product link, title, site, thumbnail,} 
    if custom == 0:
        user_name = "Balko Bot"
        avi_url = "https://cop.supply/wp-content/uploads/balkobot-1.jpg"

    webhook = Webhook.from_url(webhook_link, adapter=RequestsWebhookAdapter())
    embed = Embed(title=info_dic['product'],colour=0x272b36,url=info_dic['product-link'])
    curr_time = datetime_cyberize(str(datetime.datetime.now()))
    footer = user_name+" • "+curr_time
    embed.set_footer(text=footer,icon_url = avi_url)
    embed.set_author(name=info_dic['site'],url = info_dic['site'])
    embed.set_thumbnail(url = info_dic['thumbnail'])
    embed.add_field(name="Price",value = fields["price"])
    embed.add_field(name="Stock",value = fields["stock"])
    atc1_value = ""
    if len(fields["atc1"]) >0:
        for i in range(len(fields["atc1"])):
            atc1_value +=  "["+fields["atc1"][i][0]+"]("+fields["atc1"][i][1]+") | "+fields["atc1"][i][2]+"\n"
    else:
        atc1_value = '\u200b'

    atc2_value = ""
    
    if len(fields["atc2"]) >0:
        for i in range(len(fields["atc2"])):
            atc2_value += "["+fields["atc2"][i][0]+"]("+fields["atc2"][i][1]+") | "+fields["atc2"][i][2]+"\n"
    else:
        atc2_value = '\u200b'

    embed.add_field(name="ATC", value = atc1_value)
    embed.add_field(name="ATC", value = atc2_value)

    user = info_dic['site'] # only support https://youtube.com/ with / at the end
    user = user[8:]
    if "www." == user[:4]:
        user = user[4:]
    if "/" == user[-1]:
        user = user[:-1]

    
    webhook.send("",embed=embed,username = user,avatar_url=avi_url)




#fields{price:,stock:,atc1:[("size", "atc link","stock"),...],atc2:}
def Cyber_webhook(user_name, avi_url, webhook_link, info_dic, fields,custom): #info_dict{product link, title, site, thumbnail,} 
    if custom == 0:
        user_name = "Cyber"
        avi_url = "https://is1-ssl.mzstatic.com/image/thumb/Purple113/v4/03/44/e9/0344e9e2-3161-c993-27ef-385387c0b896/source/512x512bb.jpg"
    webhook = Webhook.from_url(webhook_link, adapter=RequestsWebhookAdapter())
    embed = Embed(title=info_dic['product'],colour=Colour.green(),url=info_dic['product-link'])
    curr_time = datetime_cyberize(str(datetime.datetime.now()))
    footer = user_name+" • "+curr_time
    embed.set_footer(text=footer,icon_url = avi_url)
    embed.set_author(name=info_dic['site'],url = info_dic['site'])
    embed.set_thumbnail(url = info_dic['thumbnail'])
    embed.add_field(name="Price",value = fields["price"])
    embed.add_field(name="Stock",value = fields["stock"])
    atc1_value = ""
    if len(fields["atc1"]) >0:
        for i in range(len(fields["atc1"])):
            
            atc1_value +=  "["+fields["atc1"][i][0]+"]("+fields["atc1"][i][1]+") | "+fields["atc1"][i][2]+"\n"
            
    else:
        atc1_value = '\u200b'

    atc2_value = ""
    
    if len(fields["atc2"]) >0:
        for i in range(len(fields["atc2"])):
            
            atc2_value += "["+fields["atc2"][i][0]+"]("+fields["atc2"][i][1]+") | "+fields["atc2"][i][2]+"\n"
            
    else:
        atc2_value = '\u200b'

    embed.add_field(name="ATC", value = atc1_value,inline = False)
    embed.add_field(name="ATC", value = atc2_value)

    user = info_dic['site'] # only support https://youtube.com/ with / at the end
    user = user[8:]
    if "www." == user[:4]:
        user = user[4:]
    if "/" == user[-1]:
        user = user[:-1]

    
    webhook.send("",embed=embed,username = user,avatar_url=avi_url)










if mode == 1 :
    
    for key in sample_info_dict.keys():

        sample_info_dict[key] = input("please input your desired "+key+": ")

    for key in sample_fields.keys():
        if key == "atc1" or key == "atc2":
            record = "1"
            sample_fields[key] = []
            while True:
                record = input("do you want to input ATC info? press 1 to continue, press 0 to stop: ")
                if record == "0":
                    break
                sz = input("please input the size: ")
                sz_url = input("please input the atc url: ")
                stock_level = input("please input the inventory: ")
                sample_fields[key].append((sz, sz_url,stock_level))
        else: 
            sample_fields[key] = input("please input your desired "+key+": ")

    if webhook_format == 1:

        Cyber_webhook(user_name= author_name, avi_url=author_icon_url,webhook_link=webhook_url,info_dic=sample_info_dict,fields= sample_fields,custom = customize)
    if webhook_format == 2:
        
        Balko_webhook(user_name= author_name, avi_url=author_icon_url,webhook_link=webhook_url,info_dic=sample_info_dict,fields= sample_fields,custom = customize)
    if webhook_format == 3:
       
        TKS_webhook(user_name= author_name, avi_url=author_icon_url,webhook_link=webhook_url,info_dic=sample_info_dict,fields= sample_fields,custom = customize)



else:
    inpo = input("please press 's' to start: ")
    site_select = int(input("select a site to monitor, 1 for packershoes, 2 for Undefeated (Upcoming): "))
    monitor_link = input("please enter the url of the product that you wanna monitor: ")
    delay = float(input('please input a desired delay, unit is seconds: '))
    new_arrival = int(input("toggle for new arrival/restock monitor (0 for NO, 1 for YES): "))
    #print("monitor will start immediately, press 'c' to exit the program")#change the input link")
    map1 = {}
    map2 = {} # for link monitor
    if new_arrival == 1:
        map3 = {} # for new arrival monitor
        map4 = {}
        new_product = ''
    while inpo == 's':

        #if keyboard.is_pressed('c'):
            # site_select = int(input("select a site to monitor, 1 for packershoes, 2 for Undefeated: "))
            # monitor_link = input("please enter the url of the product that you wanna monitor: ")
            # delay = float(input('please input a desired delay, unit is float: '))
            # print("monitor will start immediately, press 'c' to change the input link")
            # map1 = {} #resetting the map for new product monitor
            # map2 = {}
            #break
        #else: 

        if site_select == 1:
            status_check =monitor_link_packer(link = monitor_link,sizing_info_map=map1,monitor_map=map2)
            if status_check == False:
                temp_response = requests.get(monitor_link)
                send_error_msg(content=temp_response.text[:1000],url_error=webhook_url)
                break
            if new_arrival == 1:
                poo = requests.get('https://packershoes.com/products.json') 
                try:
                    p2 = json.loads(poo.text)   #check 
                except:
                    send_error_msg(content=p2.text[:1000],url_error=webhook_url)

                all_new_products = jsonpath.jsonpath(p2, "$.products")[0] #check
                if all_new_products == False:
                    send_error_msg(content=p2.text[:1000],url_error=webhook_url)
                newest = all_new_products[0] #take the newest product
                if new_product == '': # initialize the product title, monitor by product name 
                    new_product = newest['title']
                else:
                    if new_product == newest['title']:    # No updated new arrivals yet, check if stock change
                        new_link = 'https://packershoes.com/products/'+newest['handle']
                        status_check = monitor_link_packer(link = new_link, sizing_info_map = map3, monitor_map = map4)
                        if status_check == False:
                            temp_response = requests.get(new_link)
                            send_error_msg(content=temp_response.text[:1000],url_error=webhook_url)
                            print(temp_response.text)
                            break
                    else:# New product found 
                        new_product = newest['title']
                        new_link = 'https://packershoes.com/products/'+newest['handle']
                        map3 = {}
                        map4 = {}
                        status_check = monitor_link_packer(link = new_link, sizing_info_map = map3, monitor_map = map4)
                        if status_check == False:
                            temp_response = requests.get(new_link)
                            send_error_msg(content=temp_response.text[:1000],url_error=webhook_url)
                            print(temp_response.text)
                            break

                     







        time.sleep(delay)







print(datetime_cyberize(str(datetime.datetime.now())))



