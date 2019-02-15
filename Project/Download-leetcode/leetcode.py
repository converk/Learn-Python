from selenium import webdriver
from collections import defaultdict
import requests
import os
import json
import time

s = requests.session()  #创建会话对象
page=8  #提交情况的总页数
base_url = "https://leetcode-cn.com"
runtime_dict = defaultdict(list)  # 用来储存运行时间和相应的url地址

def login_leetcode(login_url, user_id, password):
	headers = {  # 请求头
		'accept': '*/*',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9',
		'referer': 'https://leetcode-cn.com/accounts/login/',
		'user-agent': 'Mozilla/5.0 (X11Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	}
	res = s.get(url=login_url, headers=headers)  # 获取crft值
	data = {
		'csrfmiddlewaretoken': res.cookies['csrftoken'],
		'login': user_id,
		'password': password,
	}
	res = s.post(url=login_url, headers=headers, data=data)  # 实际登录

def oprate_data():
	#os.mkdir("code")   #创建代码目录

	for i in range(page):
		f=open('./data/submissions-%s.json' % str(i),'r')  #打开文件

		result=json.load(f)
		submissions_dump = result['submissions_dump']
		for item in submissions_dump:
			if(item["status_display"] == "Accepted"):
				if item["title"] in runtime_dict and int(item["runtime"][:-3]) > runtime_dict[item["title"]][0]:
					pass
				else:
					if item["lang"]=="c":
						language='c'
					elif item["lang"] == "python3":
						language = 'py'
						
					runtime_dict[item["title"]].append(int(item["runtime"][:-3]))  # 将一个题目与运行时间对应起来
					runtime_dict[item["title"]].append(item["url"])  #并且储存当前提交的url地址
					runtime_dict[item["title"]].append(language)  # 并且储存当前提交的语言类型
					code_file = open("./code/%s.%s" % (item["title"], language),'w')
					code_file.close()
			else:
				pass
	f.close()
	print(runtime_dict)

def get_code(username,password):
	b = webdriver.Chrome()  #创建浏览器对象
	for (title,time_and_url) in list(runtime_dict.items())[1:]:
		print("正在爬取\"%s\"的代码" % title)
		url=base_url+time_and_url[1]  #一个提交总的url
		print(url)
		b.get(url)  #访问网址

		#模拟登陆
		b.find_element_by_name("login").send_keys(username)
		b.find_element_by_name("password").send_keys(password)
		b.find_element_by_class_name("btn-content__lOBM").click()

		print("登录成功!!")
		time.sleep(1)  #给出足够的加载时间
		#获取文本
		code=b.find_element_by_class_name("ace_content").text

		#写入文件
		f=open("./code/%s.%s" % (title,time_and_url[2]),"w")
		f.write(code)
		f.close()

def get_data_url(num):
	return 'https://leetcode-cn.com/api/submissions/?offset='+str(20*num)+'&limit=20&lastkey='

def get_data():
	for i in range(page):
		print("正在爬取第\"%d\"页数据" % i)
		res = s.get(get_data_url(i))
		f = open('./data/submissions-%s.json' % str(i), 'w')
		f.write(res.text)
		f.close()
		time.sleep(5)


# 模拟登陆
#login_leetcode('https://leetcode-cn.com/accounts/login/', 'ping', '970722hbw')
# 动态网页爬取
#get_data()
#处理数据
oprate_data()
#获取代码
get_code("ping","970722hbw")
