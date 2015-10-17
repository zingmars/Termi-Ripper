# -*- coding: utf-8-sig -*-
from bs4 import BeautifulSoup
import sys,io,time,urllib.request,pdfkit,os

#Fix for windows unicode output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,'cp437','backslashreplace')

#Statistics
questionsRipped = 0
requestsMade = 0
startTime = time.time()

#Variables
#All global because I'm not quite used to Python's scope just yet
domain = "http://csn.termi.lv"
folder = "/B/"
htmlFileName = "rip.html"
htmlFile = None
PDFFileName = "rip.pdf"

#Functions
def createHTMLFile():
	global htmlFile
	initialHTML =  """<!DOCTYPE html>
<html>
	<head> 
		<title>CSN</title>
		<meta charset="UTF-8">
		<style>
		.notice {
			text-align: right;
		}
		.correct {
			font-weight: bold;
			font-size: 1.2em;
		}
		.span6 {
			display: inline-block;
			width: 45%;
			vertical-align: top;			
		}
		img {
			margin-top: -0.5cm;
		}
		</style>
	</head>
	<body>
	<p class="notice">Ripped by <a href="https://www.github.com/zingmars/termi-ripper/">https://www.github.com/zingmars/termi-ripper/</a> from <a href="http://csn.termi.lv">http://csn.termi.lv/</a></p>
	"""
	f = open(htmlFileName, "w")
	f.write(initialHTML)
	f.close()
	htmlFile = open(htmlFileName, mode="a", encoding="utf-8") #Open the file for appending

def appendToHTML(data):
	global htmlFile
	htmlFile.write(data)

def finishHTMLFile():
	global htmlFile
	endingHTML = """
</body>
</html>"""
	htmlFile.write(endingHTML)
	htmlFile.close()

#The part that downloads each page and turns it into a HTML file
def ripSite():
	global questionsRipped
	global requestsMade
	#Get the site
	handle = None
	print("Currently downloading: " + domain+folder+"page-"+str(requestsMade+1)+"/")
	try:		
		handle = urllib.request.urlopen(domain+folder+"page-"+str(requestsMade+1)+"/")
	except:
		return False
	html = handle.read().decode("UTF-8")
	requestsMade = requestsMade + 1
	#Analyse it	
	#If it's a 404 page we finish, if not, go on.
	soup = BeautifulSoup(html, 'html.parser')	
	if soup.title.string.find("Lapa nav atrasta.") != -1:	
		return False	
	questionDiv = soup.find("div", { "class":"span9" })		

	#Get the Questions
	questionArr = questionDiv.find_all("h2")
	answerArr = questionDiv.find_all("div", {"class":"row-fluid"})
	
	counter = 0
	for question in questionArr:					
		quest = BeautifulSoup(str(question), 'html.parser').find("a").string		
		answ = str(answerArr[counter]) #Get the answers		
		#Download images
		try:
			imgSrc = BeautifulSoup(answ, 'html.parser').find_all("img")[0].get('src')
			answ = answ.replace("/media/", "media/") #This guys uses absolute paths which doesn't really work for us, so we fix it.
			if not os.path.exists(os.path.dirname(os.path.realpath(__file__))+os.path.dirname(imgSrc)): #Make directories
				os.makedirs(os.path.dirname(os.path.realpath(__file__))+os.path.dirname(imgSrc))			
			urllib.request.urlretrieve(domain+imgSrc, os.path.dirname(os.path.realpath(__file__))+imgSrc)			
		except Exception as e: #Ignore									
			pass			
				
		appendToHTML("<h1>"+str(questionsRipped+1)+". "+quest+"</h1>"+answ) #Append them to the file
		questionsRipped = questionsRipped+1
		counter = counter+1			
	return True

#Take our HTML file and convert it to a PDF file.
def htmlToPDF():
	pdfkit.from_file(htmlFileName, PDFFileName)	

#Main body
print("Ripper engaged")
createHTMLFile()
while ripSite():
	continue
finishHTMLFile()
htmlToPDF()
print("Script finished in " + str(time.time() - startTime) + " seconds. It scrapped " + str(questionsRipped) + " questions with " + str(requestsMade) + " web requests.")