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
def index():
	video_id = getVideoId('https://www.youtube.com/watch?v=M7lc1UVf-VE')
	return render_template("index.html",transcript=getSoup(video_id),embed_link="https://www.youtube.com/embed/M7lc1UVf-VE?enablejsapi=1")

@app.route('/summarize', methods=["POST"])
def getSummary():
	video_link = request.form['link']
	if(video_link != None and ('youtu.be/' in video_link) or ('youtube.com/watch?v=' in video_link)):
		video_id = getVideoId(video_link)
		print("https://www.youtube.com/embed/" + video_id + "?enablejsapi=1")
		try:
			return render_template("index.html", transcript=getSoup(video_id), embed_link="https://www.youtube.com/embed/" + video_id + "?enablejsapi=1")
		except:
			return render_template("index.html", transcript='Uh Oh! Looks like that video isn\'t supported yet', embed_link="//giphy.com/embed/uPTp0I1c3sfQs")
	else:
		return render_template("index.html", transcript='Uh Oh! Looks like that video isn\'t supported yet', embed_link="//giphy.com/embed/uPTp0I1c3sfQs")

def getVideoId(video_link):
	if(video_link != None and ('youtu.be/' in video_link) or ('youtube.com/watch?v=' in video_link)):
		beginId = video_link.index('?v=')
		video_id = video_link[beginId+3:len(video_link)]
		return video_id
	else:
		return None

def toLink(seconds,video_id):
	link = 'https://www.youtube.com/watch?v=' + video_id + '&feature=youtu.be&t=' + str(int(seconds))
	return '<a href=\"' + link + '\" target=\"_blank\"">Go to this part in the video</a>' 

def getSoup(_video_id):
	video_id = _video_id
	page = urllib.request.urlopen('http://video.google.com/timedtext?lang=en&v=' + video_id).read()

	soup = BeautifulSoup(page, 'xml')

	text_elements = soup.findAll('text')

	x = summ_it(text_elements,60,video_id)

	return x

def summ_it(elems, lapse, video_id):
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
			print("\n" + str(last_time) + " : \n" + s)
			s = summarize(s)
			s = re.sub(r'\b&#39;\b','\'',s)
			c = chunk(toLink(last_time,video_id),toPara(s))
			last_time = float(element['start'])
			data.add(c)
			s = ''
		temp_elem = re.sub(r'\n',' ',element.text)
		s +=  temp_elem + ' '

	try:
		print("\n\nflag\n\n")
		s = re.sub(r'\b\.,\b',',',s)
		print("\n" + str(last_time) + " : \n" + s)
		s = summarize(s)
		s = re.sub(r'\b&#39;\b','\'',s)
		data.add(chunk(toLink(last_time,video_id),toPara(s)))
	except:
		s = s[s.rfind('.', 0, s.rfind('.')) + 2:len(s)]
		data.add(chunk(toLink(last_time,video_id),toPara(s)))

	return_string = ''
	while(data.hasNext()):
		x = data.pop()
		return_string += (str(x.getTimestamp()) + x.getContent() + '<br>')
	return return_string

def main():
	video_id = getVideoId('https://www.youtube.com/watch?v=Qymp_VaFo9M')
	print(getSoup(video_id))
	#summarize('is Dr. Ranjit Bhagwat. Our director and editor is Nicholas Jenkins, our sound designer is Michael Aranda, and the graphics team is Thought Cafe.')

if __name__ == '__main__':
	main()