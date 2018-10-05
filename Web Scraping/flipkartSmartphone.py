from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#url="https://www.flipkart.com/search?q=smartphones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D13000&p%5B%5D=facets.ram%255B%255D%3D3%2BGB&p%5B%5D=facets.ram%255B%255D%3D2%2BGB&p%5B%5D=facets.ram%255B%255D%3D1%2BGB&p%5B%5D=facets.ram%255B%255D%3D4%2BGB&page="
url="https://www.flipkart.com/search?q=smartphones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D13000&p%5B%5D=facets.ram%255B%255D%3D3%2BGB&p%5B%5D=facets.ram%255B%255D%3D2%2BGB&p%5B%5D=facets.ram%255B%255D%3D1%2BGB&p%5B%5D=facets.ram%255B%255D%3D4%2BGB&page="
# find no of pages
my_url=url+"1"
uClient=uReq(my_url)
page_html=uClient.read()
uClient.close()
page_soup= soup(page_html,"html.parser")
containers=page_soup.find_all("div",{"class":"_2zg3yZ"})
n=int(containers[0].span.text[10:])

#lets create a file to save data
a=open("smartphonesFlipkart.csv",'w')
#a.write("Model, MRP, Price, Avalability_status, Rating, Ram_Rom, Display, Camera, Battery, processor&Battery\n")

# go through all pages and extract data
for i in range(18,n):
	my_url=url+str(i)
	uClient=uReq(my_url)
	page_html=uClient.read()
	uClient.close()
	page_soup= soup(page_html,"html.parser")
	containers=page_soup.find_all("div",{"class":"_1UoZlX"})
	print(str(i)+" "+str(len(containers)))

	
	for container in containers:
		try:
			Model=container.find_all("div",{"class":"_3wU53n"})[0].text.replace(",","|")
			if container.find_all("div",{"class":"_3auQ3N _2GcJzG"})==[]:
				MRP=container.find_all("div",{"class":"_1vC4OE _2rQ-NK"})[0].text[1:].replace(",","")
			else:MRP=container.find_all("div",{"class":"_3auQ3N _2GcJzG"})[0].text[1:].replace(",","")
			Price=container.find_all("div",{"class":"_1vC4OE _2rQ-NK"})[0].text[1:].replace(",","")
			if container.find_all("div",{"class":"_3aV9Tq"})==[]:
				Avalability_status= "Available"
			else:Avalability_status= container.find_all("div",{"class":"_3aV9Tq"})[0].text
			Rating=container.find_all("div",{"class":"hGSR34 _2beYZw"})[0].text[0:3]
			Ram_Rom=container.find_all("li",{ "class":"tVe95H"})[0].text
			Display=container.find_all("li",{ "class":"tVe95H"})[1].text
			Camera=container.find_all("li",{ "class":"tVe95H"})[2].text
			Battery=container.find_all("li",{ "class":"tVe95H"})[3].text
			#processor=container.find_all("li",{ "class":"tVe95H"})[4].text
	
			a.write(Model + "," + MRP + "," + Price + "," + Avalability_status + "," + Rating + "," + Ram_Rom + "," + Display + "," + Camera + "," + Battery + "\n")
		except: pass
a.close()