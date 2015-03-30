#!/usr/bin/env python3
import praw
import re
import string
import json

# If we're in the directory of the file, I can just get config_handler.
try:
	import config_handler
# Else, I need to get it from src.
except ImportError:
	from src import config_handler
regex = config_handler.from_config(config_handler.CONFIG_NAME, "regex")
matcher = re.compile(regex or "^wh?at$")


class LoudBot(object):
	def __init__(self, user, passw, user_agent):
		self.reddit = praw.Reddit(user_agent)
		self.reddit.login(user, passw)
		self.visited = config_handler.from_config(config_handler.VISITED_NAME)
		if not self.visited:
			self.visited = []
		self.visited = set(self.visited)

	def run(self):
		subreddit = config_handler.from_config(config_handler.CONFIG_NAME, "subreddit")
		for comm in praw.helpers.comment_stream(self.reddit, subreddit or "all", 200, verbosity=0):
			if comm.id in self.visited:
				continue
			text = self.normalize_body(comm)
			if matcher.match(text) and not comm.is_root:
				print("Got one! {}".format(comm.id))
				# I'll edit this later, when praw introduces a .parent_comment.
				parent = self.get_parent(self.reddit, comm)
				parent_text = parent.body
				reply = []
				for i in parent_text.upper().splitlines():
					reply.append("**{}**".format(i))
				reply = "\n  ".join(reply)
				comm.reply(reply)
				self.visited.add(comm.id)

	def save_visited(self):
		with open(config_handler.VISITED_NAME, "w") as visit:
			visit.write(json.dumps(list(self.visited)))

	# Helper Functions.

	@staticmethod
	def normalize_body(comment):
		body = comment.body.lower().strip()
		return "".join(i for i in body if i in string.ascii_letters)

	@staticmethod
	def get_parent(red, comment):
		return red.get_info(thing_id=comment.parent_id)
