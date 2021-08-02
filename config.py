import os

class Config(object):
	BOT_TOKEN = os.environ.get("BOT_TOKEN")
	APP_ID = int(os.environ.get("APP_ID"))
	API_HASH = os.environ.get("API_HASH")
	DATABASE_URL = os.environ.get("DATABASE_URL")
	SUDO_USERS = list(set(int(x) for x in ''.split()))
	SUDO_USERS.append(853393439)
	SUDO_USERS = list(set(SUDO_USERS))

class Messages():
      HELP_MSG = [
        ".",

         "[🔔](https://telegra.ph/file/353321e1fae6097c0f397.jpg) **FORCE SUBSCRIBE :**\n\nForce Group Members To Join A Specific Channel Before Sending Messages in The Group.\nI Will Mute Members if They Not Joined Your Channel And Tell Them To Join The Channel And Unmute Themself By Pressing A Button.",
        
        "[⚙](https://telegra.ph/file/bf0afdc7c1b3b0ab6c088.jpg) **SETUP :**\n\nFirst Of All Add Me In The Group As Admin With Ban Users Permission And In The Channel As Admin.\n● Note: Only Creator Of The Group Can Setup Me.",
        
        "[⚙](https://telegra.ph/file/353321e1fae6097c0f397.jpg) **COMMMANDS :**\n\n/ForceSubscribe - To Get The Current Settings.\n/ForceSubscribe no/off/disable - To Turn Of ForceSubscribe.\n/ForceSubscribe {Channel Username} - To Turn On And Setup The Channel.\n/ForceSubscribe clear - To Unmute All Members Who Muted By Me.\n\n● by @cw_perfect Note: /FSub Is An Alias Of /ForceSubscribe",
        
        "[👨‍💻](https://telegra.ph/file/37201b58e4f2e17f83916.jpg) **By @cw_perfect**"
      ]

      START_MSG = "**Hey [👋](https://telegra.ph/file/949e5d7d1bcaad44f6c68.jpg) [{}](tg://user?id={})**\n\n⭕️ I Can Force Members To Join A Specific Channel Before Writing Messages In The Group.\n And You Know One Thing Am A Malayalam Version\n⭕Read More At 👉 /help"
