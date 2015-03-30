# what-bot
A simple Reddit bot that solves the problem nobody ever had.

# What does it do?
Whenever somebody asks "what?" or "wat?" in a reddit comment this handy bot...  
...Well, it replies to them by SCREAMING their parent comment.

# config.json Explanation
{  
	"user": "Your Reddit Username, or rather the bot's, str",  
	"pass": "Your Reddit Password, or rather the bot's, str",  
	"regex": "What to match, the default is '^wh?at$', str",  
	"subreddit": "What subreddit to parse through, default is 'all', str",  
	"userAgent": "What user agent to use, str",
	"checkMessages": "If to check messages at startup, bool",  
	"verbose": "If to be verbose, bool",  
	"saveAll": "If to save ALL the ids or just successfull ones, bool"  
}
