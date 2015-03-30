#!/usr/bin/env python3
import src

check_msg = src.from_config(src.CONFIG_NAME, "checkMessages")
verbose = src.from_config(src.CONFIG_NAME, "verbose")
user = src.from_config(src.CONFIG_NAME, "user")
passw = src.from_config(src.CONFIG_NAME, "pass")
agent = src.from_config(src.CONFIG_NAME, "userAgent")
save_all = src.from_config(src.CONFIG_NAME, "saveAll")
bot = src.LoudBot(user, passw, agent, verbose, save_all)
if check_msg:
    bot.check_messages()
try:
    bot.run()
except KeyboardInterrupt:
    pass
finally:
    bot.save_visited()
