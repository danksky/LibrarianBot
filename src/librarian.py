import praw
import pdb
import re
import os

import librarian_logger

reddit = praw.Reddit('bot1')
comments_log_file = librarian_logger.logPath + "/" + librarian_logger.comments_log_filename + ".log"

if not os.path.isfile(comments_log_file):
	comments_replied_to = []

else:
	comments_replied_to = []
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
					librarian_logger.log_error("Bad formatting on comments_replied_to.log line " + str(line_num))
			else:
				comments_replied_to.append(comment_id) 

subreddit = reddit.subreddit('danielkawalsky')
for comment in subreddit.comments():
	comment_id = comment.id
	if comment.id not in comments_replied_to:
		if comment.body.isupper(): # Logic of Librarian
			try:
				comment.reply("Please be quiet. This is a public forum.")
				librarian_logger.log_comment(comment_id)
			except praw.exceptions.APIException as err:
				librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
				break
	else:
		print(comment_id + ": '" + comment.body + "' has already been shushed!")