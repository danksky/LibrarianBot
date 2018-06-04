import praw

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('danielkawalsky')

# for submission in subreddit.hot(limit=5):
	# print(submission.stream)
	# print("Title: ", submission.title)
	# # print("Text: ", submission.selftext)
	# print("Score: ", submission.score)
	# print("---------------------------------\n")
	# print(dir(submission))

print(dir(subreddit))

for submission in subreddit.top('week'):
	print(submission)

for submission in subreddit.hot(limit=5):
	print(submission)

print(type(subreddit.submissions()))

for comment in subreddit.comments():
	# print(comment.body)
	print(comment.submission) # get the submission of the post
	print(comment.link_url) # unnecessary because the url is: 
		# https://www.reddit.com/r/danielkawalsky/comments/8of5u8	   /garbage_post/ 
							  #(/r/<subreddit>   /comments/<comment_id>/<submission_title>/)
	break

# for submission in reddit.subreddit('danielkawalsky').hot(limit=3):
# 	for comment in submission.comments._comments:
# 		print(comment.body)
# 	break
# 	for comment in submission.comments:
# 		# print(dir(comment))
# 		# print(comment.body)
# 		break
# 	break

# # for comment in reddit.subreddit('all').stream.comments():
# 	# print(comment.text)