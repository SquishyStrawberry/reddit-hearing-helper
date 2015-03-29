#!/usr/bin/env python3
import praw
import re
import string
# If we're in the directory of the file, I can just get config_handler.
try:
	import config_handler
# Else, I need to get it from src.
except ImportError:
	from src import config_handler
matcher = re.compile(config_handler.from_config(config_handler.CONFIG_NAME, "regex") or "^wh?at$")


class LoudBot(object):
	def __init__(self, user, passw, user_agent):
		self.reddit = praw.Reddit(user_agent)
		self.reddit.login(user, passw)
		self.visited = set()
	
	def run(self):
		for comm in praw.helpers.comment_stream(self.reddit, "all", 200, verbosity=0):
			if comm.id in self.visited:
				continue
			text = self.normalize_body(comm)
			if matcher.match(text) and not comm.is_root:
				print("Got one! {}".format(comm.id))
				# I'll edit this later, when praw introduces a .parent_comment :/
				parent = self.get_parent(self.reddit, comm)
				parent_text = parent.body
				reply = "**".join(("", parent_text.upper(), ""))
				comm.reply(reply)
				self.visited.add(comm.id)

	# Helper Functions.

	@staticmethod
	def normalize_body(comment):
		body = comment.body.lower().strip()
		return "".join(i for i in body if i in string.ascii_letters)

	@staticmethod
	def get_parent(red, comment):
		return red.get_info(thing_id=comment.parent_id)
	
		
