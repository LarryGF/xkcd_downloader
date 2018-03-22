#!python3
#Download all XKCD comics

#This concept can be used to download all XKCD web comics, but it can be tweaked to download the web comics from 9gags, or Cyanide and Happiness, for instance
#
#the url of the comic is given by the <href> attribute of an <img> element
#the <img> element is inside a <div id="comic"> element
#the Prev button has a rel HTML attribute with the value prev
#the first comic's Prev button links to http://xkcd.com/#

import requests, os, bs4


os.makedirs('xkcd',exist_ok=True)

try:
	last = open('last','r')

except:
	last = open('last','w')
	last.write('\n')
	

url = last.read()

if url == '\n' or url =='':
	url = 'http://xkcd.com'  
	
	
else:	
	print('Resuming from: ' + url)
	
 
while not url.endswith('#'):
	print('Connecting to the webpage %s' %url)
	res = requests.get(url)
	res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text)

	comicElem = soup.select('#comic img')
	if comicElem == []:
		print('Could not find the comic image')

	else:
		comicUrl = 'http:' + comicElem[0].get('src')
		print('Downloading image %s' %(comicUrl))
		res = requests.get(comicUrl)
		res.raise_for_status()

		imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close()

	prevLink = soup.select('a[rel="prev"]')[0]
	url = 'http://xkcd.com' + prevLink.get('href')
	last = open('last','w')
	last.write(url)
	last.close()

last = open('last','w')
last.write('\n')
last.close()

print('Done')
