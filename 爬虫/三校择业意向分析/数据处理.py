import csv
import re
import copy
tag={} #以字典的形式存放分类标签
tag_num={}
def Data_processing_CHENGDIAN():
	Title=[]
	Company=[]
	Date=[]
	Post=[]
	rf=open("CHENGDIAN_1.csv","r",encoding="utf-8")
	reader=csv.reader(rf)
	for i,row in enumerate(reader):
		if i!=0:
			title,company,date=row
			Title.append(title.strip())
			Company.append(company.strip())
			Date.append(date)
	rf.close()
	with open("CD_D.csv", "w", encoding="utf-8", newline="") as f:
		csvf = csv.writer(f)
		csvf.writerow(["序号","招聘主题", "用人单位", "发布日期", "浏览次数"])
		for i in range(len(Title)):
			csvf.writerow([i+1,Title[i], Company[i], Date[i], 0])
			Post.append([Title[i],Company[i],0,1])
	f.close()
	tag_match(Post,"成电")
	return Title,Company
def Data_processing_XIDIAN():
	Title=[]
	Company=[]
	Date=[]
	View_Count=[]
	Post=[]
	rf=open("XIDIAN_1.csv","r",encoding="utf-8")
	reader=csv.reader(rf)
	for i,row in enumerate(reader):
		if i!=0: #从csv文件第二行开始读取，即不读表头
			title,company,date,view_Count=row
			Title.append(title.strip())
			Company.append(company.strip())
			Date.append(date) #日期本身即为YYYY-MM-DD格式
			View_Count.append(int(view_Count))
	with open("XD_D.csv", "w", encoding="utf-8", newline="") as f:
		csvf = csv.writer(f)
		csvf.writerow(["序号","招聘主题", "用人单位", "发布日期", "浏览次数"])
		for i in range(len(Title)):
			csvf.writerow([i+1,Title[i], Company[i], Date[i], View_Count[i]])
			Post.append([Title[i], Company[i], View_Count[i], 1])
	data=[]
	with open('XD_D.csv', 'r+',encoding="utf-8") as f:
		reader = csv.reader(f)
		for i,line in enumerate(reader):
			if i!=0:
				data.append(line)
		data.sort(key=lambda item: int(item[4]), reverse=True)
		#以第四列数据（浏览次数）为依据进行降序排序
	f.close()
	with open("最受西电学生关注的招聘TOP20.csv", "w", newline='',encoding="utf-8") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["序号", "招聘主题", "用人单位", "发布日期", "浏览次数"])
		for i in range(0,20):
			writer.writerow(data[i])
	csvfile.close()
	tag_match(Post, "西电")
	return Title,Company
def Data_processing_BEIYOU():
	Title=[]
	Company=[]
	Date=[]
	View_Count=[]
	Position_num = []
	Post=[]
	rf = open("BEIYOU_1.csv", "r", encoding="utf-8")
	reader = csv.reader(rf)
	for i, row in enumerate(reader):
		if i != 0: #从csv文件第二行开始读取，即不读表头
			title, company, date, view_Count,position_num = row
			Title.append(title.strip())
			Company.append(company.strip())
			Date.append(date) #日期本身即为YYYY-MM-DD的格式
			View_Count.append(int(view_Count))
			if position_num=='':
				Position_num.append(1)
			else :Position_num.append(int(position_num))
	with open("BY_D.csv", "w", encoding="utf-8", newline="") as f:
		csvf = csv.writer(f)
		csvf.writerow(["序号", "招聘主题", "用人单位", "发布日期", "浏览次数","职位数量"])
		for i in range(len(Title)):
			csvf.writerow([i + 1, Title[i], Company[i], Date[i], View_Count[i],Position_num[i]])
			Post.append([Title[i],Company[i],View_Count[i],Position_num[i]])
	data1 = []  # 按浏览次数排序
	data2=[] #按职位数量排序
	with open('BY_D.csv', 'r+',encoding="utf-8") as f:
		table = []
		reader = csv.reader(f)
		for i,line in enumerate(reader):
			if i!=0:
				table.append(line)
		data1 = sorted(table, key=lambda item: int(item[4]), reverse=True)
		data2=sorted(table, key=lambda item: int(item[5]), reverse=True)
	f.close()
	with open("最受北邮学生关注的招聘TOP20.csv", "w", newline='',encoding="utf-8") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["序号", "招聘主题", "用人单位", "发布日期", "浏览次数","职位数量"])
		for i in range(0,20):
			writer.writerow(data1[i])
	csvfile.close()
	with open("北邮招聘职位总数、招聘职位数量TOP10.csv", "w", newline='',encoding="utf-8") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["序号", "招聘主题", "用人单位", "发布日期", "浏览次数","职位数量"])
		for i in range(0,10):
			writer.writerow(data2[i])
	csvfile.close()
	tag_match(Post, "北邮")
	return Title,Company
def Classify():
	file = open("分类.txt", encoding="UTF-8")
	while True:
		text = file.readline()
		if not text:
			break
		else:
			tag[text.split(":")[0]] = text.split(":")[1].split(",")
	for item in tag:  # 去掉换行符
		t = tag[item][-1]
		tag[item][-1] = t.strip()
		tag_num[item]=[0,0,0] #个数,浏览次数,招聘职位个数
		#tag_num为一个字典类型全局变量，键为雇主类型，值为一个列表:[个数，浏览次数，招聘职位个数]
		#在此定义tag_num，便于后续数据处理
	file.close()
def csv4(Title_CD,Company_CD,Title_XD,Company_XD,Title_BY,Company_BY):
	Title=[]
	Company=[]
	Item={}
	for i in Title_XD,Title_CD,Title_BY:
		Title.extend(i)
	for i in Company_XD,Company_CD,Company_BY:
		Company.extend(i)
	for i in range(len(Title)):
		Item[Title[i]]=[Company[i],'']
	# 利用字典的特性进行去重，当标题名称相同时，用后面的来覆盖前面的
	for i in Item: #以公司名称为标准对雇主类型分类
		for tag_name in tag:
			for item in tag[tag_name]:
				if len(re.findall(item, Item[i][0])) != 0:
					# 当匹配到相应的关键词时，打上标签
					Item[i][1]=tag_name
					break
	with open("CAT_A.csv", "w", newline='', encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow(["序号", "招聘主题", "雇主类型"])
		i=1
		for item in Item:
			writer.writerow([i,item,Item[item][1]])
			i+=1
	f.close()
def tag_match(Post,schoolname):
	tmp_tagNum=copy.deepcopy(tag_num)
	ICT=[]
	for i in range(0,len(Post)):
		for tag_name in tag:
			for item in tag[tag_name]:
				if len(re.findall(item,Post[i][1]))!=0:#匹配关键词
					tmp_tagNum[tag_name][0]+=1
					#统计该雇主类型数量
					tmp_tagNum[tag_name][1]+=Post[i][2]
					#统计该雇主类型对应浏览次数
					if (tag_name=="互联网类")or (tag_name=="通信类"):#统计ICT行业
						ICT.append([Post[i][0],Post[i][1],Post[i][2],Post[i][3]])#主题,浏览次数,职位个数
					if (schoolname=="北邮"):#若为北邮，统计职位数量
						tmp_tagNum[tag_name][2]+=Post[i][3]
					break
	_ICT(ICT,schoolname)
	sorted_tagNum = sorted(tmp_tagNum.items(), key=lambda item:(int(item[1][1]),int(item[1][0])),reverse=True)
	#雇主类型数量，浏览次数两重排序，雇主类型数量优先，相同时浏览次数高的排在前面
	with open("最受{}学生关注的雇主类型TOP10.csv".format(schoolname), "w", newline='',encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow(["雇主类型", "数量","浏览总数","排名"])
		for i in range(0,10):
			writer.writerow([sorted_tagNum[i][0],sorted_tagNum[i][1][0],sorted_tagNum[i][1][1],i+1])
	f.close()
	if (schoolname=="北邮"):#北邮招聘职位所属雇主类型TOP10
		sorted_tagNum_ByPositionNum = sorted(tmp_tagNum.items(), key=lambda item: (int(item[1][2])), reverse=True)
		#按招聘职位数量排序
		with open("北邮招聘职位所属雇主类型TOP10.csv", "w", newline='', encoding="utf-8") as f:
			writer = csv.writer(f)
			writer.writerow(["雇主类型", "招聘职位", "排名"])
			for i in range(0, 10):
				writer.writerow([sorted_tagNum_ByPositionNum[i][0], sorted_tagNum_ByPositionNum[i][1][2], i + 1])
		f.close()
def _ICT(ICT,schoolname):
	ICT.sort(key=lambda item:(int(item[2]),int(item[3])),reverse=True) #按浏览次数、职位个数，两重排序
	with open("{}最关注ICT行业的招聘主题TOP10.csv".format(schoolname), "w", newline='', encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow(["招聘主题", "招聘公司","浏览次数", "职位数量","排名"])
		for i in range(0, 10):
			writer.writerow([ICT[i][0], ICT[i][1], ICT[i][2],ICT[i][3],i + 1])
	f.close()
Classify()
Title_CD,Company_CD=Data_processing_CHENGDIAN()
Title_XD,Company_XD=Data_processing_XIDIAN()
Title_BY,Company_BY=Data_processing_BEIYOU()
csv4(Title_CD,Company_CD,Title_XD,Company_XD,Title_BY,Company_BY)
