import praw
import config
import time
import csv
import os

ourComment = "This is good for Butt Coin."
subreddits = ["all","bitcoin","cryptocurrency","nanocurrency","nanotrade","test"]
fileName = "replied.csv"#this file contains id of comments/posts that we have already replied to
numRemembered = 1000; #how many comment id or post id to store in the csv
numfound = 0;
numreplied = 0;

def CheckText(text,id):
	global numfound
	global numreplied
	mentioned =  "butcoin" in text or "Butcoin" in text
	if mentioned: numfound += 1
	replied = str(id) in repliedIds
	if mentioned and replied: 
		numreplied +=1

	return (mentioned and not replied)

def BotLogin():	
	out = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.clientId,
			client_secret = config.secret,
			user_agent = "good for bitcoin bot v0.1")
	return out

def RunBot(info,subName):
	ourSub = info.subreddit(subName)
	global numfound
	global numreplied
	numfound = 0
	numreplied = 0
	print("browsing subreddit: " + subName)

	for comment in ourSub.comments(limit=25):
		if CheckText(comment.body,comment.id) and comment.body != ourComment:
			try:
				comment.reply(ourComment)
				print("replied to comment " + str(comment.id)+"\n")
				AppendId(comment.id)
			except:
				OverCommentError()
				return

	for post in ourSub.new(limit=25):
		if CheckText(post.title,post.id):
			try:
				post.reply(ourComment)
				print("replied to post " + str(post.id)+"\n")
				AppendId(post.id)
			except:
				OverCommentError()
				return
	SaveIds()
	ReportFound()

def ReportFound():
	global numfound
	global numreplied
	print("we found " + str(numfound) + " matching posts/comments")
	print("replied: " + str(numreplied))
	print("new: " + str(numfound-numreplied))
	print("")

def AppendId(id):
	global repliedIds
	repliedIds.insert(0,str(id))
	repliedIds = repliedIds[:numRemembered]

def SaveIds():
	global repliedIds
	global fileName
	with open(fileName, 'w' ,newline = '') as csvfile:
		csvfile.seek(0)
		csvfile.truncate()
		writer = csv.writer(csvfile, delimiter = ',')
		for item in repliedIds:
			writer.writerow([item])


def CSVToList():
	global fileName
	with open(fileName, newline = '') as csvfile:
		reader = csv.reader(csvfile)
		outList = []
		for row in reader:
			outList.append(row[0])

	return outList

def OverCommentError():
	ReportFound()
	print("we are trying to comment too much")
	print ("pausing for 10 minutes...")
	time.sleep(10*60)
		

repliedIds = CSVToList()

while True:
	redditInfo = BotLogin()
	for sub in subreddits:
		RunBot(redditInfo,sub)
	print ("bot has completed a search. Pausing for 1 minute...")
	time.sleep(60)

