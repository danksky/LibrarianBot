import praw

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('askreddit')

print(dir(subreddit))

for submission in subreddit.top('week'):
	print(submission)

for submission in subreddit.hot(limit=5):
	print(submission)

print(type(subreddit.submissions()))

for comment in subreddit.comments():
	# print(comment.body)
	print(comment.submission) # get the submission of the post
	print(comment.link_url)
	print(comment.link_permalink)
	break

comment = reddit.comment('e039ste')
ancestor = comment
refresh_counter = 0
while not ancestor.is_root:
    ancestor = ancestor.parent()
    if refresh_counter % 9 == 0:
        ancestor.refresh()
    refresh_counter += 1
print('Top-most Ancestor: {}'.format(ancestor))