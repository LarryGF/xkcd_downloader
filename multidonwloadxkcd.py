
import os, requests, bs4, threading

os.makedirs('xkcd', exist_ok=True)

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


def downloadxkcd(startcomic, endcomic):
    
	for urlNumber in range(startcomic, endcomic):
		print('Connecting to the webpage %s' %urlNumber)
		res = requests.get('http://xkcd.com/' + str(urlNumber))
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


#Create and start the Thread objects.
downloadThreads = []

for i in range(0,2100,100):   # loop 21 times, create 21 threads
	downloadThread = threading.Thread(target=downloadxkcd, args=(i+1, i+99))
	downloadThreads.append(downloadThread)
	downloadThread.start()

# Wait all threads to end
for downloadThread in downloadThreads:
	downloadThread.join()

last = open('last','w')
last.write('\n')
last.close()

print('Done')





