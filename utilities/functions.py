"""----------------- Variables --------------------- """
acc_guild_ids = [942681097504960542]
main_thumbnail = "https://media.discordapp.net/attachments/946057540687515658/991807221891604631/a_d62f1e4ad0ffbd6539be39542d9c404a.webp"
"""----------------- Functions --------------------- """

def get_time(seconds):
	weeks, seconds = divmod(seconds, 604800)
	days, seconds = divmod(seconds, 86400)
	hours, seconds = divmod(seconds, 3600)
	minutes, seconds = divmod(seconds, 60)

	types = {"weeks": weeks, "days": days, "hours": hours, "minutes": minutes, "seconds": seconds}
	
	text = list("".join(
		f"{(types[i])} {i if types[i] > 1 else i[:-1]}? "
		if types[i] else ""
		for i in types)[:-2])
	
	for v, i in enumerate(text):
		if i == "?":
			text[v] = "," if text.count("?") > 1 else " and"
			
	return "".join(text)