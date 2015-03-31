#!/usr/bin/env python3
import praw
import re
import string
import json
import time
import random

# If we're in the directory of the file, I can just get config_handler.
try:
	import config_handler
# Else, I need to get it from src.
except ImportError:
	from src import config_handler
regex = config_handler.from_config(config_handler.CONFIG_NAME, "regex")
matcher = re.compile(regex or "^wh?at$")
italics = re.compile("^\*[^\*]+\*$")


class LoudBot(object):
	def __init__(self, user, passw, user_agent, save_all=False, verbose=True):
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
		self.save_all = save_all

	def run(self):
		"""
		Main code for the bot.
		Runs indefinitely, or at least until an error.
		"""
		if self.verbose:
			print("Starting bot...")
		subreddit = config_handler.from_config(config_handler.CONFIG_NAME, "subreddit")
		for comm in praw.helpers.comment_stream(self.reddit, subreddit or "all", 200, verbosity=0):
			try:
				successful = False
				if comm.id in self.visited or comm.is_root or comm.author == self.reddit.user:
					continue
				text = self.normalize_body(comm)
				if matcher.match(text):
					if self.verbose:
						print("Got one! {}".format(comm.id))
					# I'll edit this later, when praw introduces a .parent_comment.
					parent = self.get_parent(self.reddit, comm)
					parent_text = parent.body.upper().strip()
					reply = []
					for i in parent_text.splitlines():
						asterisks = 2 + (1 if italics.search(i) else 0)
						reply.append("{0}{1}{0}".format("*"*asterisks, i))
					reply = "\n  ".join(reply)
					comm.reply(reply)
					successful = True
				if successful or self.save_all:
					self.visited.add(comm.id)

			except praw.errors.APIException as e:
				# Let's just save face and wait a while.
				print("Oops! Got an error '{}'!".format(e))
				if isinstance(e, praw.errors.RateLimitExceeded):
					time.sleep(e.sleep_time)
				else:
					minutes = random.randint(1, 5)
					time.sleep(60*minutes)

	def save_visited(self):
		"""
		Saves whatever's in self.visited
		"""
		lvisited = list(self.visited)
		lvisited = self.pretty_json(lvisited)
		with open(config_handler.VISITED_NAME, "w") as config_file:
			config_file.write(lvisited)

	def check_messages(self):
		"""
		Checks through the messages, and can reply/read them.
		"""
		if self.verbose:
			print("Checking messages...")
		messages = tuple(self.reddit.get_unread())
		empty = len(messages) < 1
		for i in messages:
			# No verbose flag for this one, since without printing this would be useless.
			itype = "comment" if isinstance(i, praw.objects.Comment) else "message"
			print("Got a {}!".format(itype))
			do_open = input("Do you want to read it?\n> ").lower().strip()
			if do_open.startswith("y"):
				print(i.body)
				do_reply = input("Do you want to reply?\n> ").lower().strip()
				if do_reply.startswith("y"):
					reply_with = input("With what?\n> ")
					if reply_with:
						i.reply(reply_with)
			i.mark_as_read()
		if empty:
			print("No messages found.")

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
		Arguments:
			red: a praw.Reddit instance
			comment: a praw.objects.Comment instance
		Return:
			The parent comment of arg comment.
		"""
		return red.get_info(thing_id=comment.parent_id)

	@staticmethod
	def pretty_json(l):
		"""
		Prettifies JSON
		Arguments:
			l: A list, or other iterable supported in JSON
		Return:
			The Pretty JSON version of l
		"""
		jl = json.dumps(l, sort_keys = True)
		jl = jl.split(",")
		return ",\n".join(map(lambda x: x.strip(), jl))
