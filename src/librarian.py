import praw
import schedule
import time
from random import randint
import smtplib
from email.mime.text import MIMEText

import password_manager
import librarian_logger

comments_replied_to 		= []
comments_replied_to_roots	= []
submission_commented_in		= []
reddit = None 

EMAIL_ALERT_PASSWORD = password_manager.librarian_gmail_pass

def initiate_librarian():
	print(str(time.ctime()) + " Initiating librarian...")
	global reddit
	reddit = praw.Reddit('bot1')
	librarian_logger.set_logger_printtoconsole(True)
	comments_replied_to 		= librarian_logger.populate_log_list(librarian_logger.COMMENT_TYPE)
	comments_replied_to_roots	= populate_roots(comments_replied_to)
	submission_commented_in 	= librarian_logger.populate_log_list(librarian_logger.SUBMISSION_TYPE)
	# traverse_subreddits()

def traverse_subreddits():
	print(str(time.ctime()) + " running...")
	reply_count, reply_limit = 0, 5
	subreddits = [
		'anticonsumption',
		'bettereveryloop',
		'oddlysatisfying',
		'beamazed',
		'television',
		'nonononoyes',
		'macroporn',
		'meditation',
		'getmotivated',
		'natureisfuckinglit',
		'urbanexploration',
		'showerthoughts', 
		'askreddit', 
		'murderedbywords', 
		'mildlyinteresting', 
		'wholesomememes', 
		'eyebleach', 
		'trees', 
		'madlads', 
		'space', 
		'theydidthefuckyou',
		'unexpected',
		'todayilearned'] # banned from r/hmmm lol
	while(len(subreddits) > 0 and reply_count <= reply_limit):
		random_index = randint(0, len(subreddits)-1)
		subreddit_title = subreddits[random_index]
		print("Now trying to quiet a redditor in: " + subreddit_title)
		if quiet_a_redditor(subreddit_title):
			reply_count += 1
		subreddits.remove(subreddit_title)

def quiet_a_redditor(subreddit_title):
	global reddit
	query_count, query_limit = 0, 1000
	time_limit = 120 # seconds
	shushes = [
		"Please be quiet.", 
		"Please take your 9.5 down to a 3.5.", 
		"Please keep it down.", 
		"Could you keep it down please?", 
		"Please lower your voice."]

	# Query the comments of chose subreddit
	subreddit = reddit.subreddit(subreddit_title) 
	retrieved_comments = set()
	time_start = time.time()
	for comment in subreddit.stream.comments():
		if (time.time() - time_start > time_limit):
			print("Timeout @ " + str(time.ctime()))
			break
		comment_id = comment.id
		if (comment_id in retrieved_comments): # Hopefully prevents repeated comments in the stream
			continue
		else:
			retrieved_comments.add(comment_id)
		if comment.id not in comments_replied_to:
			query_count += 1
			if query_count <= query_limit:
				if query_count > query_limit/2:
					print("Reached " + str(query_limit/2) + " queried comments.")
				if merits_a_shush(comment.body):
					root_id = get_root_comment(comment_id)
					if distinct_tree(root_id):
						try:
							# Magic
							comment.reply(shushes[randint(0, len(shushes)-1)] + " This is a public forum.")
							# Local/Runtime record
							comments_replied_to.append(comment_id)
							comments_replied_to_roots.append(root_id)
							submission_commented_in.append(comment.submission)
							# Permanent record
							librarian_logger.log_comment(comment.link_permalink, comment_id)
							librarian_logger.log_submission(comment.submission)
							return True # For now, success means you're done in the subreddit
						except praw.exceptions.APIException as err:
							librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
							break
						except prawcore.exceptions.Forbidden as err:
							librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
							break
						except prawcore.exceptions.InvalidToken as err:
							# reddit 		= praw.Reddit('bot1')
							librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
							notify()
							break
						except prawcore.exceptions.ResponseException as err:
							librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
							notify()
							break
					else:
						print("Found " + comment_id + " to shush, but I've already shushed their tree!")
			else:
				print("Reached " + str(query_limit) + " queried comments on subreddit " + subreddit_title + ".")
				break
		else:
			print(comment_id + ": '" + comment.body[:10] + "' has already been shushed!")
	return False

def notify():
	# Notify me!
	msg = MIMEText("(Attempted " + comment_id + ") " + str(err))
	msg['Subject'] = 'Error attempting to reply to comment: ' + comment_id
	msg['From'] = 'librarian@loc.gov'
	msg['To'] =   'librarianbot.reddit@gmail.com'
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('librarianbot.reddit@gmail.com', EMAIL_ALERT_PASSWORD)
	server.send_message(msg)
	server.quit()

def distinct_tree(attempt_root_id):
	return (attempt_root_id not in comments_replied_to_roots)

def get_root_comment(comment_id):
	global reddit
	comment = reddit.comment(comment_id)
	ancestor = comment
	refresh_counter = 0
	while not ancestor.is_root:
	    ancestor = ancestor.parent()
	    if refresh_counter % 9 == 0:
	        ancestor.refresh()
	    refresh_counter += 1
	return str(ancestor)

def populate_roots(comments_replied_to):
	for comment_id in comments_replied_to:
		comments_replied_to_roots.append(get_root_comment(comment_id))

def merits_a_shush(text): # Logic of Librarian
	return (text.isupper()) and (len(text) > 6)
	# return (len(text) > 10 and text.count('s') > 4) # dummy test

def schedule_librarian(job):
	schedule.every().day.at("02:30").do(job)
	schedule.every().day.at("09:30").do(job)
	schedule.every().day.at("13:30").do(job)
	schedule.every().day.at("17:30").do(job)
	schedule.every().day.at("20:30").do(job)
	schedule.every().day.at("23:30").do(job)	

if __name__ == "__main__":
	initiate_librarian()
	schedule_librarian(traverse_subreddits)
	while True:
		schedule.run_pending()
		time.sleep(1)