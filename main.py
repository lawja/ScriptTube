from bs4 import BeautifulSoup
import urllib.request
import re
from gensim.summarization import summarize

import LinkedLists as ll

class chunk:

	def __init__(self, ts, cont):
		self.timestamp = ts
		self.content = cont

	def getTimestamp(self):
		return self.timestamp;

	def getContent(self):
		return self.content

	def __str__(self):
		print(self.timestamp + " : " + self.content)

def toPara(passage):
	return '<p>' + passage + '</p>'

page = urllib.request.urlopen('http://video.google.com/timedtext?lang=en&v=EcQ-6Zd1638').read()

soup = BeautifulSoup(page, 'xml')

t = soup.findAll('text')

chunk_lapse = 60

next_time = 60

data = ll.LinkedList()

s = ''

y = 0

last_time = 0

for e in t:
	current_time = float(e['start']);
	if(not(current_time <= next_time)):
		next_time = float(e['start']) + float(chunk_lapse)
		s = re.sub(r'\b\.,\b',',',s)
		s = summarize(s)
		s = re.sub(r'\b&#39;\b','\'',s)
		c = chunk(last_time,toPara(s))
		last_time = float(e['start'])
		data.add(c)
		s = ''
	el = re.sub(r'\n',' ',e.text)
	s +=  el + ' '

s = re.sub(r'\b\.,\b',',',s)
s = summarize(s)
s = re.sub(r'\b&#39;\b','\'',s)
data.add(chunk(last_time,toPara(s)))

while(data.hasNext()):
	x = data.pop()
	print(str(x.getTimestamp()) + " : " + x.getContent())

