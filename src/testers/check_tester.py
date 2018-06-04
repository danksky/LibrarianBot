import praw
import pdb
import re
import os
import logging

if not os.path.isfile("../../logs/comments_replied_to.log"):
	comments_replied_to = []

else:
	comments_replied_to = []
	with open("../../logs/comments_replied_to.log", "r") as f:
		lines = f.read().split("\n")
		for line in lines:
			comment_id = line[-9:-2]
			if len(comment_id) > 7:
				print("Error") # TODO: error log
			comments_replied_to.append(line[-9:-2]) 
