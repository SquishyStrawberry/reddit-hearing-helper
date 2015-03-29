#!/usr/bin/env python3
import praw
import re
import string
import config_handler
matcher = re.compile(config_handler.from_config(config_handler.CONFIG_NAME, "regex") or "wh?at")


class LoudBot(object):
	def __init__(self, user_agent):
		self.reddit = praw.Reddit(user_agent)
		self.visited = set()
	
	def run(self):
		for comm in praw.helpers.comment_stream(self.reddit, "all", 200):
			text = self.normalize_body(comm)
			if matcher.match(text):
				parent_text = comm.parent.body
				reply = "**".join(("", parent_text.upper(), ""))
				print(reply)	

	@staticmethod
	def normalize_body(comment):
		body = comment.body.lower().strip()
		return "".join(i for i in body if i in string.ascii_letters)

	
		
