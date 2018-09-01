import praw
import config

ourComment = "this is good for bitcoin"
def CheckText(text):
	return "bitcoin" in text or "Bitcoin" in text or "BTC" in text

def BotLogin():	
	out = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.clientId,
			client_secret = config.secret,
			user_agent = "good for bitcoin bot v0.1")
	return out

def RunBot(info):
	ourSub = info.subreddit('cryptocurrency')
	for comment in ourSub.comments(limit=25):
		if CheckText(comment.body) and comment.body != ourComment:
			print("comment found")
			comment.reply(ourComment)


	for post in ourSub.new(limit=25):
		if CheckText(post.title):
			print("post found")
			post.reply(ourComment)

redditInfo = BotLogin()
RunBot(redditInfo)