#!/usr/bin/env python3
import src
import warnings

check_msg = src.from_config(src.CONFIG_NAME, "checkMessages")
verbose = src.from_config(src.CONFIG_NAME, "verbose")
user = src.from_config(src.CONFIG_NAME, "user")
passw = src.from_config(src.CONFIG_NAME, "pass")
agent = src.from_config(src.CONFIG_NAME, "userAgent")
save_all = src.from_config(src.CONFIG_NAME, "saveAll")
bot = src.LoudBot(user=user, passw=passw, user_agent=agent, save_all=save_all, verbose=verbose)
if check_msg:
    bot.check_messages()
try:
    # Just to ignore the ResourceWarning from PRAW
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        bot.run()
except KeyboardInterrupt:
    pass
finally:
    bot.save_visited()
