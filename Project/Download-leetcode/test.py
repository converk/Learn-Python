from selenium import webdriver
import time

b=webdriver.Chrome()
b.get('https://leetcode-cn.com/submissions/detail/11839382/')

#模拟登陆
print(1)
b.find_element_by_name("login").send_keys("ping")
print(2)
b.find_element_by_name("password").send_keys("970722hbw")
print(3)
b.find_element_by_class_name("btn-content__lOBM").click()
print(4)
time.sleep(5)
print(b.current_url)
print(b.find_element_by_class_name("ace_content").text)