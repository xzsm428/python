from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

def Get_data():
	page = webdriver.Edge() #选择浏览器
	Title=[]#招聘主题
	Company=[] #用人单位
	Date=[] #发表日期
	j=1
	page = webdriver.Edge()  # 选择浏览器
	while 1:
		url = "https://jiuye.uestc.edu.cn/career/info/otherRec.html?page={}&".format(j)
		page.get(url)
		time.sleep(0.5)
		for i in range(1,21):
			page.implicitly_wait(5)
			Current_Date=page.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/table/tbody/tr[{}]/td[3]".format(i)).text
			if Current_Date!="2021-08-31":
				Date.append(Current_Date)
				Title.append(page.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/table/tbody/tr[{}]/td[1]".format(i)).text)
				Company.append(page.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/table/tbody/tr[{}]/td[2]".format(i)).text)
				page.implicitly_wait(5)
			else:
				return Title,Company,Date
		j+=1

Title = []  # 招聘主题
Company = []  # 用人单位
Date = []  # 发表日期
Title,Company,Date=Get_data()

with open("CHENGDIAN_1.csv","w",encoding="utf-8",newline="") as f:
	csvf = csv.writer(f)
	csvf.writerow(["招聘主题", "用人单位", "发布日期", "浏览次数"])
	for i in range(len(Title)):
		csvf.writerow([Title[i],Company[i],Date[i],])