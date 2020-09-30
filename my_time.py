def TimeLeft(allFrames, madeFrames, spentTime):
	return int((allFrames - madeFrames) * spentTime / madeFrames)

def HoursLeft(seconds):
	return str(seconds // 3600) + "h "

def MinutesLeft(seconds):
	return str((seconds // 60) - (seconds // 3600) * 60) + "m "

def Seconds(seconds):
	return str(seconds - (seconds // 60) * 60 - (seconds // 3600) * 3600) + "s "