from bs4 import BeautifulSoup
import urllib.request
import re
from gensim.summarization import summarize
from flask import Flask, redirect, render_template, request, session, url_for

import LinkedLists as ll

app = Flask(__name__,template_folder='templates')

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

@app.route('/')
def index(_name="jake"):
	return render_template("index.html",name=_name)

def toPara(passage):
	return '<p>' + passage + '</p>'

def getSoup():
	page = urllib.request.urlopen('http://video.google.com/timedtext?lang=en&v=EcQ-6Zd1638').read()

	soup = BeautifulSoup(page, 'xml')

	text_elements = soup.findAll('text')

	summ(text_elements,60)

def summ(elems, lapse):
	chunk_lapse = lapse

	next_time = chunk_lapse + 1

	data = ll.LinkedList()

	s = ''

	y = 0

	last_time = 0

	for element in elems:
		current_time = float(element['start']);
		if(not(current_time <= next_time)):
			next_time = float(element['start']) + float(chunk_lapse)
			s = re.sub(r'\b\.,\b',',',s)
			s = summarize(s)
			s = re.sub(r'\b&#39;\b','\'',s)
			c = chunk(last_time,toPara(s))
			last_time = float(element['start'])
			data.add(c)
			s = ''
		temp_elem = re.sub(r'\n',' ',element.text)
		s +=  temp_elem + ' '

	s = re.sub(r'\b\.,\b',',',s)
	s = summarize(s)
	s = re.sub(r'\b&#39;\b','\'',s)
	data.add(chunk(last_time,toPara(s)))

	while(data.hasNext()):
		x = data.pop()
		#print(str(x.getTimestamp()) + " : " + x.getContent())

def main():
	getSoup()

if __name__ == '__main__':
	main()

