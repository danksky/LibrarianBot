import praw
import pdb
import re
import os
import schedule
import time
from random import randint

import librarian_logger

comments_replied_to = []
submission_commented_in = []
reddit = praw.Reddit('bot1')

def initiate_librarian():
	print(str(time.ctime()) + " running...")
	comments_log_file = librarian_logger.logPath + "/" + librarian_logger.comments_log_filename + ".log"
	submissions_log_file = librarian_logger.logPath + "/" + librarian_logger.submissions_log_filename + ".log"
	# Populate comments log list
	if os.path.isfile(comments_log_file):
		with open(comments_log_file, "r") as f:
			lines = f.read().split("\n")
			# Clean
			while('' in lines):
				lines.remove('')
			# Iterate through id's
			line_num = -1
			for line in lines:
				line_num += 1
				comment_id = line[-9:-2]
				if ((len(comment_id) > 7) or (re.match('^[0-9A-Za-z]+$', comment_id) is None)):
					# Something is up with the read
					if (len(comment_id) == 0):
						librarian_logger.log_error("Comment id is being grabbed from empty line") # Meaning cleaning above didn't work
					else:
						librarian_logger.log_error("Bad formatting on " + comments_log_file + " line " + str(line_num) + ":\n\t" + line)
				else:
					comments_replied_to.append(comment_id) 
	# Populate submissions log list
	if os.path.isfile(submissions_log_file):
		with open(submissions_log_file, "r") as f:
			lines = f.read().split("\n")
			# Clean
			while('' in lines):
				lines.remove('')
			# Iterate through id's
			line_num = -1
			for line in lines:
				line_num += 1
				submission_id = str(line[-8:-2])
				if ((len(submission_id) > 6) or (re.match('^[0-9A-Za-z]+$', submission_id) is None)):
					# Something is up with the read
					if (len(submission_id) == 0):
						librarian_logger.log_error("Comment id is being grabbed from empty line") # Meaning cleaning above didn't work
					else:
						librarian_logger.log_error("Bad formatting on " + submissions_log_file + " line " + str(line_num) + ":\n\t" + line)
				else:
					submission_commented_in.append(submission_id) 
	traverse_subreddits()

def traverse_subreddits():
	reply_count, reply_limit = 0, 5
	subreddits = [
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
		'todayilearned',
		'hmmm']
	while(len(subreddits) > 0 and reply_count <= reply_limit):
		random_index = randint(0, len(subreddits)-1)
		subreddit_title = subreddits[random_index]
		print("Now trying to quiet a redditor in: " + subreddit_title)
		if quiet_a_redditor(subreddit_title):
			reply_count += 1
		subreddits.remove(subreddit_title)

def quiet_a_redditor(subreddit_title):
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
					try:
						# Magic
						comment.reply(shushes[randint(0, len(shushes)-1)] + " This is a public forum.")
						librarian_logger.log_comment(comment.link_permalink, comment_id)
						librarian_logger.log_submission(comment.submission)
						return True # For now, success means you're done in the subreddit
					except praw.exceptions.APIException as err:
						librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
						break
			else:
				print("Reached " + str(query_limit) + " queried comments on subreddit " + subreddit_title + ".")
				break
		else:
			print(comment_id + ": '" + comment.body[:10] + "' has already been shushed!")
	return False

def merits_a_shush(text): # Logic of Librarian
	return (text.isupper()) and (len(text) > 6)

def schedule_librarian(job):
	schedule.every().day.at("10:30").do(job)
	schedule.every().day.at("5:30").do(job)

if __name__ == "__main__":
	 # initiate_librarian()
	schedule_librarian(initiate_librarian)
	while True:
		schedule.run_pending()
		time.sleep(1)

    
