from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import re
import time

def Get_data():
	url = 'https://job.bupt.edu.cn/frontpage/bupt/html/recruitmentinfoList.html?type=1'
	page = webdriver.Edge() #选择浏览器
	page.get(url)
	Title=[]#招聘主题
	Company=[] #用人单位
	Date=[] #发表日期
	View_count=[] #浏览次数
	Position_num=[] #职位数量
	t=8
	s=1
	while 1:
		Position_nums = page.find_elements(By.XPATH, "//*[@id='listPlace']/div/div[2]/p")
		for position in Position_nums:
			if re.findall("\d*(?=个)", position.text):
				Position_num.append(re.findall("\d*(?=个)", position.text)[0])
			else:Position_num.append("")
		for i in range(1,16):
			page.implicitly_wait(5)
			url1=page.find_element(By.XPATH,"//div[@class='infoItem collected recmmonded'][{}]/div[@class='left']/a[@class='tit']".format(i)).get_attribute('href')
			js = 'window.open("{}");'.format(url1)
			page.execute_script(js)
			page.implicitly_wait(5)
			page.switch_to.window(page.window_handles[-1])
			str1=page.find_element(By.CSS_SELECTOR, "div.midInfo > div").text
			if re.findall("(?<=日期：)\d\d\d\d-\d\d-\d\d",str1)[0]!="2021-08-31":
				Date.append(re.findall("\d\d\d\d-\d\d-\d\d",str1)[0])
				Title.append(page.find_element(By.XPATH,"//div[@class='name getCompany']").text)
				Company.append(page.find_element(By.XPATH,"//div[@class='infoTop']/a[@class='name']").text)
				View_count.append(re.findall("(?<=次数：)\d*", str1)[0])
				page.close()
				page.switch_to.window(page.window_handles[0])
				page.implicitly_wait(5)
			else:
				return Title,Company,Date,View_count,Position_num
		if s==3: t=9
		if s==4:t=10
		s += 1
		next_page=page.find_element(By.XPATH,"//div[@class='pageWrap']/ul[@class='fPage']/li[{}]/a".format(t))
		page.execute_script("arguments[0].click();", next_page)
		time.sleep(0.5)

Title = []  # 招聘主题
Company = []  # 用人单位
Date = []  # 发表日期
View_count = []  # 浏览次数
Position_num=[] #职位数量
Title,Company,Date,View_count,Position_num=Get_data()

with open("BEIYOU_1.csv","w",encoding="utf-8",newline="") as f:
	csvf = csv.writer(f)
	csvf.writerow(["招聘主题", "用人单位", "发布日期", "浏览次数", "职位数量"])
	for i in range(len(Title)):
		csvf.writerow([Title[i],Company[i],Date[i],View_count[i],Position_num[i]])