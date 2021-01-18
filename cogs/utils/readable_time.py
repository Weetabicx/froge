import math


def readable_time(inital):
	"""Turns the commands.OnCooldown.retry_after into a readable format for users"""
	days = 0
	hours = 0
	minutes = 0
	seconds = 0

	if inital > (60*60*24):
		days = int(math.floor(inital/(60*60*24)))
		inital -= days*(60*60*24)

	if inital > 3600:
		hours = int(math.floor(inital/3600))
		inital -= hours*3600

	if inital > 60:
		minutes = int(math.floor(inital/60))
		inital -= minutes*60

	if inital > 0:
		seconds = inital
		inital -= seconds
		
	return f"{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"
