#!/usr/bin/env python3
import src

def logged_in(reddit_instance):
	return reddit_instance.user is not None and reddit_instance.authentication_ is not None

def reply_to_comment(reddit, comment):
	if not logged_in(reddit):
		return -1
	reply_with = src.make_reply(comment)
	appendix = src.get_from_config(src.CONFIG_NAME, "extra")
	if reply_with is not None and comment.author != reddit.user:
		reply_with = "**".join(("", reply_with, ""))  # Hack-ish way to wrap.
		comment.reply(reply_with + appendix)
		return 0
	return 1
