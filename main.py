import requests
from bs4 import BeautifulSoup
import re

# Create the URL with your specified requirements.
species = 'cats' # options: 'cats', dogs', 'small-animals', 'farm-animals', 'all'
minAge = 0
maxAge = 1 # max: 10
pageNum = 0
url = ('https://www.spca.nz/adopt?species=' 
	+ species + '&centres=all&breed=all&size=all&animal_id=&minAge=' 
	+ str(minAge) + '&maxAge=' 
	+ str(maxAge) + '&minActivity=&maxActivity=&pageNum=' 
	+ str(pageNum))

# Get the contents of the first page.
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all(class_ = 'card-link card-link--adopt')

pages = len(soup.find_all('li', class_ = 'pagination-item item'))
for i in range(1, pages+1):
	url = url[:-1] + str(i)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = results + soup.find_all(class_ = 'card-link card-link--adopt')


mydict = dict() # key: ID; values: name, age, location, link, breed, gender
				# could have multiple animals with same name

for elem in results:
	name = elem.find('h3', class_ ='js-animal-title').text

	if (name == 'Kittens - None Available At This Time'): 
		continue

	age = elem.find('h4', class_ ='card-subtitle--age').text

	# if (int(age[0]) > 6):
	# 	continue
	if (int(re.search("[0-9]+", age).group(0)) > 4): # 4 month old or younger only
		continue

	location = elem.find('h4', class_ ='card-subtitle--centre').text
	link = "https://www.spca.nz" + elem['href']
	ID = re.search("\/[0-9]+\/", link).group(0)[1:-1]

	if (name == "Kittens Available For Adoption"):
		breed = elem.find('h4', class_ = 'card-subtitle--gender-breed').text
		mydict[ID] = [name, age, location, link, breed, None, 1]
	else:
		genderbreed = elem.find('h4', class_ = 'card-subtitle--gender-breed').text
		gender = genderbreed[0:genderbreed.index(" ")]
		breed = genderbreed[genderbreed.index(" ") + 1:]
		mydict[ID] = [name, age, location, link, breed, gender, 1]

print(mydict)
