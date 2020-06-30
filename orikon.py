import datetime
import requests

from bs4 import BeautifulSoup


# type(ja,jsなど)とyyyyとmmからランキングページリストを取得
def getPageList(type,year,month):
	url = "https://www.oricon.co.jp/rank/RankNavigationCalendar.php?kbn="+type+\
		"&type=w&date="+str(year)+"-"+str(month)+"-1&url_date="+str(year)+"-"+str(month)+"-1&trigger=change"
	html = requests.get(url).content
	soup = BeautifulSoup(html, "html.parser")
	options = soup.find("div",class_="block-rank-search-box")
	options = options.find("div",class_="wrap-select-week")
	options = options.find("select").find_all("option")
	result=[]
	for option in options:
		result.append(option.get("value"))
	return result

#指定URLのランキングページから、max_pageで指定したページ数分取得
def getRanking(url,max_page=1):
	result=""
	for i in range(max_page):
		result+=parsePage(url+"p/"+str(i+1)+"/")
	return result

#指定URLのページをパース
def parsePage(url):
	result = ""
	html = requests.get(url).content
	soup = BeautifulSoup(html, "html.parser")
	sections = soup.find_all("section")
	for	section in sections:
		data = section.find("div",class_="inner")
		if data.find("a")!=None:
			data=data.find("a")
			url = "https://www.oricon.co.jp"+data.get("href")
		else:
			url=""
		title = data.find("div").find("h2").text
		artist = data.find("div").find("p").text
		date = data.find("div").find("ul").find("li").text
		date = date[date.find("2"):date.find("2")+11]
		if(date.find("2019年")>=0):
			continue				#昨年以前の作品はいらないので省く
		result+=artist+"\t"+title+"\t"+date+"\t"+url+"\n"
	return result


pages = getPageList("ja",2020,6)
result=""
for page in pages:
	result+=getRanking(page,2)
	result+="\n"
print(result)
