from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import re
import time

def Get_data():
	# edge_options = webdriver.EdgeOptions()
	# edge_options.add_argument('--headless')
	# page = webdriver.Edge(options=edge_options)
	Title=[]#招聘主题
	Company=[] #用人单位
	Date=[] #发表日期
	View_count=[] #浏览次数
	j=1
	page = webdriver.Edge()  # 选择浏览器
	url="https://job.xidian.edu.cn/job/search?domain=xidian&d_category%5B0%5D=0&d_category%5B1%5D=100&d_category%5B2%5D=101&d_category%5B3%5D=102"
	page.get(url)
	time.sleep(0.5)
	Last_page = re.findall("(?<=page=)\d*",page.find_element(By.XPATH, "//*[@id='yw0']/li[9]/a").get_attribute('href'))[0]
	while 1:
		Item_Num=page.find_elements(By.XPATH,"//div[@class='left']/div[@class='job']/div[@class='name']/a")
		for i in range(1,len(Item_Num)+1):
			page.implicitly_wait(5)
			Current_Date=re.findall("\d\d\d\d-\d\d-\d\d",page.find_element(By.XPATH,"//li[{}]/div[@class='left']/div[@class='job']/div[@class='name']/span".format(i)).text)[0]
			Current_Company=page.find_element(By.XPATH,"//li[{}]/div[@class='left']/div[@class='job']/div[@class='company']/a".format(i)).text
			Current_Title=page.find_element(By.XPATH,"//li[{}]/div[@class='left']/div[@class='job']/div[@class='name']/a".format(i)).text
			Date.append(Current_Date)
			Title.append(Current_Title)
			Company.append(Current_Company)
			page.find_element(By.XPATH,"//li[{}]/div[@class='left']/div[@class='job']/div[@class='name']/a".format(i)).click()
			page.switch_to.window(page.window_handles[-1])
			View_count.append(re.findall("(?<=：)\d*",page.find_element(By.XPATH,"//div[1]/div/div[2]/div/ul/li[1]").text)[0])
			page.implicitly_wait(10)
			page.close()
			page.switch_to.window(page.window_handles[0])
		if int(Last_page)!=j:
			j += 1
			url = "https://job.xidian.edu.cn/job/search?domain=xidian&d_category%5B0%5D=0&d_category%5B1%5D=100&d_category%5B2%5D=101&d_category%5B3%5D=102&page={}".format(j)
			page.get(url)
			time.sleep(0.5)
		else: return Title,Company,Date,View_count


Title = []  # 招聘主题
Company = []  # 用人单位
Date = []  # 发表日期
View_count = []  # 浏览次数
Title,Company,Date,View_count=Get_data()

with open("XIDIAN_1.csv","w",encoding="utf-8",newline="") as f:
	csvf = csv.writer(f)
	csvf.writerow(["招聘主题", "用人单位", "发布日期", "浏览次数"])
	for i in range(len(View_count)):
		csvf.writerow([Title[i],Company[i],Date[i],View_count[i]])