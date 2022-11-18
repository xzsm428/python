import requests
from requests.structures import CaseInsensitiveDict
from lxml import etree
import json
inform=[]
for i in range(1,6):
	url = "https://bj.fang.lianjia.com/loupan/pg{}/".format(i)

	headers = CaseInsensitiveDict()
	#最重要的：User-Agent和Referer，Accept
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"

	r=requests.get(url,headers=headers)
	content=r.text

	sel=etree.HTML(content)
	all_rooms=sel.xpath("//div[@class='resblock-desc-wrapper']")
	for room in all_rooms:
		room_name=room.xpath(".//div[@class='resblock-name']/a")
		room_area=room.xpath(".//div[@class='resblock-area']/span")
		room_NumOfRoom=room.xpath(".//a[@class='resblock-room']/span")#加’.'从当前为根进行匹配
		s=room_name[0].text+"---"
		#print(room_name[0].text,"---",end="")
		for item in room_NumOfRoom:
			s+=item.text.strip()+'/'
			#print(item.text.strip(),'/',end="")
		s+="---"
		#print("---",end="")
		#print(room_area[0].text)
		if (type(room_area[0].text)==str):
			s+=room_area[0].text
		inform.append(s)
#print(inform)
filename = '链家新房数据.json'
with open(filename, "w", encoding="utf-8") as f:
	for item in inform:
		json_str = json.dumps(item, ensure_ascii=False) + "\n"
		f.write(json_str)