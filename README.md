# 📁 File Store Bot

<div align="center">

<img src="https://yt3.googleusercontent.com/p9g9i5N55WgCn1mFFjl8iut4BOd0O4RRjn7WB_Silj9JmJ42tE-yhdZ0oR_7m-F4kGHT22Br=s176-c-k-c0x00ffffff-no-rj" 
width="150" 
style="border-radius: 12px;" />

<br><br>

<a href="https://t.me/teamjb1">
  <img src="https://img.shields.io/badge/TEAM--JB%20CHANNEL-blue?style=for-the-badge&logo=telegram" />
</a>

<a href="https://t.me/botsupdatesgroup">
  <img src="https://img.shields.io/badge/UPDATE%20GROUP-blue?style=for-the-badge&logo=telegram" />
</a>

</div>

Telegram Bot to store posts and documents accessible via special links.

## 🚀 Overview

File Sharing Token Bot is a Telegram bot designed to store posts and documents, accessible through special links. This bot provides a convenient way to manage and share content within Telegram.

### ✨ Features

- Store posts and documents.
- Access content via special links.
- Easy to deploy and customize.
- Token Verifiction
- Auto Deletion

## 🛠️ Setup

To deploy the bot, follow these steps:

1. Add the bot to a database channel with all permissions.
2. Add the bot to the ForceSub channel as an admin with "Invite Users via Link" permission if ForceSub is enabled.

## 📦 Installation

### Deploy on Heroku

Click the button below to deploy the bot on Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Deploy on Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/1jKLr4)

### Deploy on Koyeb

Click the button below to deploy the bot on Koyeb:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/teamjassbeniwal-ctrl/your_repo&branch=main&name=file-sharing-bot)

### Deploy on Your VPS

```bash
git clone https://github.com/teamjassbeniwal-ctrl/File_Store_Bot_TeamJB
cd file-sharing-token-bot
pip3 install -r requirements.txt
# <Create config.py appropriately>
python3 main.py
````

🔧 Admin Commands

```
start - start the bot or get posts

id - get your Telegram User ID and account details

myplan - check your current subscription plan and expiry date

plans - view available premium plans and pricing

👑 Admin Commands
⚠️ These commands are restricted to bot administrators only.

batch - create link for more than one posts

genlink - create link for one post

addpremium - add user to premium.

removepremium - remove user from premium.

users - view bot statistics

broadcast - broadcast any messages to bot users

stats - checking your bot uptime
```

🛠️ Variables

* `API_HASH` Your API Hash from my.telegram.org
* `APP_ID ` Your API ID from my.telegram.org
* `TG_BOT_TOKEN` Your bot token from @BotFather
* `OWNER_ID` Must enter Your Telegram Id
* `CHANNEL_ID` Your Channel ID eg:- -100xxxxxxxx
* `DB_URI ` Your mongo db url
* `DB_name ` Your mongo db session name ( random )
* `ADMINS` Optional: A space separated list of user_ids of Admins, they can only create links
* `START_MESSAGE` Optional: start message of bot, use HTML.
* `FORCE_SUB_MESSAGE`Optional:Force sub message of bot, use HTML and Fillings
* `FORCE_SUB_CHANNEL` Optional: ForceSub Channel ID, leave 0 if you want disable force sub
* `PROTECT_CONTENT` Optional: True if you need to prevent files from forwarding
* `AUTO_DELETE_TIME` Optional: True Delete time in seconds
### Extra Variables

* `CUSTOM_CAPTION` put your Custom caption text if you want Setup Custom Caption, you can use HTML for formatting (only for documents)
* `DISABLE_CHANNEL_BUTTON` Put True to Disable Channel Share Button, Default if False
* `BOT_STATS_TEXT` put your custom text for stats command, use HTML
* `USER_REPLY_TEXT` put your text to show when user sends any message, use HTML

### Token Variables

* `IS_VERIFY` = Default : "True" (if you want off : False )
* `SHORTLINK_URL` = Your shortner Url ( ex. "api.shareus.io")
* `SHORTLINK_API` = Your shortner API (ex. "PUIAQBIFrydvLhIzAOeGV8yZppu2")
* `VERIFY_EXPIRE` = ( ex. 86400)) # Add time in seconds

### Premium Varible 
* `PREMIUM_TEXT` = "🎉 Congratulations! You are now a Premium User."
* `PREMIUM_EXPIRE_TEXT` = "⚠️ Your Premium Plan has expired. Please renew to continue."
* `PLANS_TEXT` = "💎 Available Plans:\n\n7 Days - ₹49\n30 Days - ₹149\nLifetime - ₹499"
* `PREMIUM_BYPASS_VERIFY` = True

### Fillings

#### START_MESSAGE | FORCE_SUB_MESSAGE

* `{first}` - User first name
* `{last}` - User last name
* `{id}` - User ID
* `{mention}` - Mention the user
* `{username}` - Username

#### CUSTOM_CAPTION

* `{filename}` - file name of the Document
* `{previouscaption}` - Original Caption

#### CUSTOM_STATS

* `{uptime}` - Bot Uptime

 
📁 Example .env File 

TG_BOT_TOKEN=
APP_ID=
API_HASH=
OWNER_ID=
CHANNEL_ID=
DATABASE_URL=
DATABASE_NAME=

IS_VERIFY=True
SHORTLINK_URL=
SHORTLINK_API=
VERIFY_EXPIRE=86400
FREE_TIME=10800

FORCE_SUB_CHANNEL=0
AUTO_DELETE_TIME=60
PROTECT_CONTENT=False

💬 Support
Join Our [Telegram Group](https://www.telegram.dog/botsupdatesgroup) For Support/Assistance And Our [Channel](https://www.telegram.dog/teamjb1) For Updates.   
   
Report Bugs, Give Feature Requests There..   

🎉 Credits

Thanks to Dan for his awesome library. [Libary](https://github.com/pyrogram/pyrogram)
Our support group members.


## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

You are free to:
- Use
- Modify
- Distribute

❗ But you MUST:
- Share source code
- Keep same license (GPL). 


   **Star this Repo if you Liked it ⭐⭐⭐**

