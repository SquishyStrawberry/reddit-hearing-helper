#!/usr/bin/env python3
import string


def normalize(text):
	# Never modify the original value!
	text_ = text.lower().strip()
	return "".join(i for i in text_ if i in string.ascii_letters)


def is_valid(comment):
	body = normalize(comment.body)
	return body == "what"

def make_reply(comment):
	# Still check if it's valid.
	# I do trust YOU to make sure you can reply.
	if is_valid(comment):
		parent = comment.parent
		parent_text = parent.body
		return parent_text.upper()
	return None  # I don't know why I do it explicitly.


	
