#!/usr/bin/python3
#sudo apt install python3-pip
#sudo apt install python3-pandas
#sudo pip3 install bs4
import numpy as np
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import folium

#
#Статистика
#

url1 = 'http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&root=178400312&tvd=27820001217428&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217428&type=222'
url2='http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&root=178401812&tvd=27820001217432&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217432&type=222'
url3='http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&root=178402412&tvd=27820001217440&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217440&type=222'

def parse(url):
	response = urllib.request.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, "lxml")
	table = soup.find('table', style='width:100%;border-color:#000000')
	left = table.find('table', align='left')
	right = table.find('table', style='width:100%;overflow:scroll')
	rowsr = right.find_all('tr')
	rowsl = left.find_all('tr')[1:]
	rowsl.remove(rowsl[11])
	rowsr.remove(rowsr[12])
	result = []
	for col in rowsr[0].find_all('td'):
		result.append([col.text])
	for row in rowsr[1:]:
		i=0
		for col in row.find_all('td'):
			result[i].append(col.nobr.b.text)
			i=i+1
	for row in rowsr[12:]:
		i=0
		for col in row.find_all('td'):
			a=col.text.split('\n')
			s=a[1].split('%')
			result[i].append(s[0])
			i=i+1
	#return(pd.DataFrame(result))
	return(result)

#
#Графики
#


"""1-кол-во избирателей; 3-явка; 12, 13, 14, 15, 16, 17- голоса и проценты за Амосова, Беглова и Тихонову"""
res1=np.array(parse(url1))
res2=np.array(parse(url2))
res3=np.array(parse(url3))
res=np.vstack((res1,res2,res3))
res=pd.DataFrame(res)
x=res[3]
y1=res[15]
y2=res[16]
y3=res[17]
#print(res)

for i in range(res.shape[0]):                   
	for j in range(1,res.shape[1]):
		res[j][i]=float(res[j][i])
for i in range(res.shape[0]):
	res[3][i]=100*res[3][i]/res[1][i]
				
plt.scatter(x,y1, color='red', s=3, label='Амосов')
plt.scatter(x,y2, color='green', s=3, label='Беглов')
plt.scatter(x,y3, color='blue', s=3, label='Тихонова')
plt.title('Зависимость голосов за кандидатов от явки')
plt.xlabel('Явка %')
plt.ylabel('% голосов')
plt.legend()
plt.show()

x=res[1]
y=res[3]
plt.scatter(x, y, s=3, color='black')
plt.title('Зависимость явки от количества избирателей на участке')
plt.xlabel('Кол-во избирателей')
plt.ylabel('Явка %')
plt.show()

uch=[0]
tol=[]
count=[0]
k=0
for i in range(res.shape[0]):
	tol.append(int(res[3][i]))

for i in range(len(tol)):
	flag=0
	for j in range(k+1):
		if tol[i]==uch[j]:
			count[j]+=1
			flag=1
	if flag==0:
		uch.append(tol[i])
		count.append(1)
		k+=1
plt.scatter(uch, count, color='blue', s=10)
plt.title('Зависимость количества участков от явки')
plt.xlabel('Явка %')
plt.ylabel('Кол-во участков')
plt.show()

#
#Карта
#

response = open('Карта УИК Санкт-Петербурга.kml')
html = response.read()
soup = BeautifulSoup(html, "lxml")
YIK = soup.find_all('name')
YIKs=[]
for i in YIK:
	YIKs.append(i.text)
del YIKs[0]
del YIKs[0]

Koord = soup.find_all('coordinates')
Shirota=[]
Dolgota=[]
for i in Koord:
	c=i.text.split(',')
	Dolgota.append(float(c[1]))
	d=c[0].strip()
	Shirota.append(float(d))

N=len(YIKs)
YIKlast=[]
Dolg=[]
Shir=[]
for i in range(N):
	if (float(YIKs[i]) > 198 and float(YIKs[i]) < 245) or (float(YIKs[i]) > 251 and float(YIKs[i]) < 316) or (float(YIKs[i]) > 329 and float(YIKs[i]) < 402):
		YIKlast.append(YIKs[i])
		Dolg.append(Dolgota[i])
		Shir.append(Shirota[i])
#print(YIKlast)
#print(len(Dolg))
#print(len(Shir))

map = folium.Map(location=[60.051322, 30.340559], zoom_start = 12)
for i in range(len(Shir)):
	folium.CircleMarker(location = [Dolg[i],Shir[i]], radius=0.4*res[15][i], popup=str(res[15][i])+" %", color='green', fill_color='green', fill_opacity=0.01*res[15][i]).add_to(map) 
map.save("Amosov.html")

map = folium.Map(location=[60.051322, 30.340559], zoom_start = 12)
for i in range(len(Shir)):
	folium.CircleMarker(location = [Dolg[i],Shir[i]], radius=0.2*res[16][i], popup=str(res[16][i])+" %", color='blue', fill_color='blue', fill_opacity=0.01*res[16][i]).add_to(map)
map.save("Beglov.html")

map = folium.Map(location=[60.051322, 30.340559], zoom_start = 12)
for i in range(len(Shir)):
	folium.CircleMarker(location = [Dolg[i],Shir[i]], radius=0.4*res[17][i], popup=str(res[17][i])+" %", color='red', fill_color='red', fill_opacity=0.01*res[17][i]).add_to(map)
map.save("Tihonova.html")

map = folium.Map(location=[60.051322, 30.340559], zoom_start = 12)
for i in range(len(Shir)):
	folium.CircleMarker(location = [Dolg[i],Shir[i]], radius=0.4*res[3][i], popup=str(res[3][i])+" %", color='red', fill_color='red', fill_opacity=0.01*res[3][i]).add_to(map)
map.save("Attandance.html")




	
