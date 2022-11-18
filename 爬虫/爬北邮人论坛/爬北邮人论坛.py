#请在PyCharm控制台中按提示输入用户名和密码
#帖子时间以发布时间为准

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import csv

def Get_Time_Yesterday():
	time_now=datetime.datetime.now()
	time_str=str(time_now.year)+'-'
	if len(str(time_now.month))==1:
		time_str+='0'+str(time_now.month)+'-'
	else:
		time_str+=str(time_now.month)+'-'
	if len(str(time_now.day))==1:
		time_str+='0'+str(time_now.day-1)
	else:
		time_str+=str(time_now.day-1)
	return time_str

url = 'https://bbs.byr.cn/index' #北邮人首页网址
page = webdriver.Edge() #选择浏览器
page.get(url)
user_name = page.find_element(By.CSS_SELECTOR,'input[name="id"]')
id=input("请输入用户名:")
user_name.send_keys(id)
user_pwd = page.find_element(By.CSS_SELECTOR,'input[name="passwd"]')
passwd=input("请输入密码:")
user_pwd.send_keys(passwd)
time.sleep(1)
login_button = page.find_element(By.CSS_SELECTOR,'input[id="b_login"]')
login_button.submit()
time.sleep(3)
page.find_element(By.XPATH,"//li[@id='section-3']/div[@class='widget-head']/span[@class='widget-title']/a[2]").click()
time.sleep(3)
page.find_element(By.XPATH,"//table/tbody/tr[18]/td[1]/a").click()
time.sleep(3)
time_yesterday=Get_Time_Yesterday()
Title=[]
for i in range(1,6):#最多向前翻5页
	Item_Title=page.find_elements(By.XPATH,"//*[@id='body']/div[3]/table/tbody/tr[*]/td[2]/a")
	time.sleep(1)
	Item_Date=page.find_elements(By.XPATH,"//*[@id='body']/div[3]/table/tbody/tr[*]/td[3]")
	time.sleep(1)
	for j in range(len(Item_Date)):
		if Item_Date[j].text==time_yesterday:
			Title.append(Item_Title[j].text)
	if i==1:
		page.find_element(By.XPATH,"//li[11]/a").click()
	else:
		page.find_element(By.XPATH,"//li[12]/a").click()
	time.sleep(3)

with open("BYR-JOB-YYYY-MM-DD.csv","w",encoding="utf-8",newline="") as f:
	csvf = csv.writer(f)
	for i in range(len(Title)):
		csvf.writerow([i+1,Title[i]])