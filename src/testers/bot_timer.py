import praw
import time

reddit = praw.Reddit('bot1')
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
	'todayilearned',] # banned from r/hmmm lol

time_taken = {}
subreddit_comments = {}
query_prospect = {}

for subredditTitle in subreddits:
	print("Querying " + subredditTitle)
	subreddit = reddit.subreddit(subredditTitle)
	time_start = time.time()
	query_count, query_limit = 0, 100
	comment_ids = set()
	for comment in subreddit.stream.comments():
		query_count += 1
		comment_ids.add(comment.id)
		if query_count == query_limit:
			time_taken[subredditTitle] = time.time() - time_start
			print("Took " + str(time_taken[subredditTitle]) + " seconds to get " + str(query_limit) + " queries.")
			break
	subreddit_comments[subredditTitle] = comment_ids


for subredditTitle in subreddits:
	print("Querying " + subredditTitle)
	subreddit = reddit.subreddit(subredditTitle)
	time_start = time.time()
	query_count, query_limit = 0, 100
	comment_ids2 = set()
	for comment in subreddit.stream.comments():
		query_count += 1
		if (comment.id not in set(subreddit_comments[subredditTitle])):
			comment_ids2.add(comment.id)
		if query_count == query_limit:
			time_taken[subredditTitle] = time.time() - time_start
			break
	print(str(len(comment_ids2)) + " ids not queried in the first run (2)")

for subredditTitle in subreddits:
	print("Querying " + subredditTitle)
	subreddit = reddit.subreddit(subredditTitle)
	time_start = time.time()
	query_count, query_limit = 0, 100
	comment_ids3 = set()
	for comment in subreddit.stream.comments():
		query_count += 1
		if (comment.id not in set(subreddit_comments[subredditTitle])):
			comment_ids3.add(comment.id)
		if query_count == query_limit:
			time_taken[subredditTitle] = time.time() - time_start
			break
	print(str(len(comment_ids3)) + " ids not queried in the first run (3)")

for subredditTitle in subreddits:
	print("Querying " + subredditTitle)
	subreddit = reddit.subreddit(subredditTitle)
	time_start = time.time()
	query_count, query_limit = 0, 100
	comment_ids4 = set()
	for comment in subreddit.stream.comments():
		query_count += 1
		if (comment.id not in set(subreddit_comments[subredditTitle])):
			comment_ids4.add(comment.id)
		if query_count == query_limit:
			time_taken[subredditTitle] = time.time() - time_start
			break
	print(str(len(comment_ids4)) + " ids not queried in the first run (4)")


print(time_taken)