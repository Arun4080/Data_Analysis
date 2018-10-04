from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url="https://www.newegg.com/global/in/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=graphics+card&N=-1&isNodeId=1"

# Opening Url and grabing the page
uClient = uReq(my_url)
page_html=uClient.read()
uClient.close()

# Open file for saving csv
a=open("CSV_Files/graphics_Details.csv",'w')
header="brand, product_name, Price\n"
a.write(header)


# html parsing
page_soup= soup(page_html,"html.parser")
containers=page_soup.find_all("div",{"class":"item-container"})
for container in containers:
	brand=container.div.div.a.img["title"]
	title_container=container.find_all("a",{"class":"item-title"})
	title=title_container[0].text
	price_container=container.find_all("li",{"class":"price-current"})
	price=price_container[0].text[4:10].strip()

	print("brand: " + brand.replace(",",""))
	print("title: " + title.replace(",","|"))
	print("price: " + price.replace(",",""))
	print(" ")

	a.write(brand.replace(",","") + "," + title.replace(",","|") + "," + price.replace(",","") + "\n" )

a.close()
