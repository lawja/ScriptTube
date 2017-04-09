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
def index(transcript=''):
	return render_template("index.html",transcript=getSoup())

def toPara(passage):
	return '<p>' + passage + '</p>'

def toLink(seconds,video_id):

def getSoup():
	video_id = 'EcQ-6Zd1638'
	page = urllib.request.urlopen('http://video.google.com/timedtext?lang=en&v=' + video_id).read()

	soup = BeautifulSoup(page, 'xml')

	text_elements = soup.findAll('text')

	x = summ(text_elements,60,video_id)

	return x

def summ(elems, lapse, video_id):
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

	return_string = ''
	while(data.hasNext()):
		x = data.pop()
		return_string += (str(x.getTimestamp()) + " : " + x.getContent() + '<br><br>')
	return return_string

def main():
	getSoup()
	toLink(10,video_id)

if __name__ == '__main__':
	main()