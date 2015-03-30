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
	def __init__(self, user, passw, user_agent, verbose=True):
		"""
		Initializes the LoudBot class
		Arguments:
			user[str]: The username of whatever user the bot will use.
			passw[str]: The password of said user.
			user_agent[str]: What user agent to use for the reddit instance
			verbose[bool]: Sets whether or not to print anything at all.
		"""
		self.reddit = praw.Reddit(user_agent)
		self.reddit.login(user, passw)
		self.visited = config_handler.from_config(config_handler.VISITED_NAME)
		if not self.visited:
			self.visited = []
		self.visited = set(self.visited)
		# I don't use the logging module because I don't like how it works
		# when you use requests.
		self.verbose = verbose

	def run(self):
		"""
		Main code for the bot.
		Runs indefinitely, or at least until an error.
		"""
		if self.verbose:
			print("Starting bot.")
		subreddit = config_handler.from_config(config_handler.CONFIG_NAME, "subreddit")
		for comm in praw.helpers.comment_stream(self.reddit, subreddit or "all", 200, verbosity=0):
			if comm.id in self.visited:
				continue
			text = self.normalize_body(comm)
			if matcher.match(text) and not comm.is_root:
				if self.verbose:
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
		"""
		Saves whatever's in self.visited
		"""
		with open(config_handler.VISITED_NAME, "w") as visit:
			visit.write(json.dumps(list(self.visited)))

	def check_messages(self):
		"""
		Checks through the messages, and can reply/read them.
		"""
		for i in self.reddit.get_unread():
			# No verbose flag for this one, since without printing this would be useless.
			print("Got a message!")
			do_open = input("Do you want to read it?\n> ").lower().strip()
			if do_open.startswith("y"):
				print(i.body)
				do_reply = input("Do you want to reply?\n> ").lower().strip()
				if do_reply.startswith("y"):
					reply_with = input("With what?\n> ")
					if reply_with:
						i.reply(reply_with)
			i.mark_as_read()


	# Helper Functions.

	@staticmethod
	def normalize_body(comment):
		"""
		Normalizes the body of a comment
		Arguments:
			comment: a praw.objects.Comment instance.
		"""
		body = comment.body.lower().strip()
		return "".join(i for i in body if i in string.ascii_letters)

	@staticmethod
	def get_parent(red, comment):
		"""
		Gets the parent of a comment
		arguments:
			red: a praw.Reddit instance
			comment: a praw.objects.Comment instance
		"""
		return red.get_info(thing_id=comment.parent_id)
