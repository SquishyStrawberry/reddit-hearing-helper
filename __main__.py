#!/usr/bin/env python3
import src

bot = src.LoudBot(src.from_config(src.CONFIG_NAME, "user"), src.from_config(src.CONFIG_NAME, "pass"), "Py3 LoudBot")
try:
    bot.run()
finally:
    bot.save_visited()
