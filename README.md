# Discord-Bot-Watchdog
**A Discord Bot that can warn a User via DM if a overwatched Bot goes offline**

###Featurelist

- [x] Distinguish between bot users and normal users
- [x] Notify multiple users possible
- [x] Notify multiple channels possible
- [x] Notify on offline and online event
- [x] Spam prevention (If a Bot is still online but just changing its status text)
- [ ] Switchable Mailer (In future Versions)


### Config Example
**At the first start the config-directory and the confugartions-file will be created.
In the config.ini settings can be made.
E.g. which bots are monitored. In addition, users and channels can be entered, which should be notified in the event of a failure.
(With each entry several entries are possible... each separated by a space)**
```
[Settings]
token = 
bot_prefix = !
owner_id = 000000000000000000

[Subscribers]
users = 000000000000000000 000000000000000000
channels = 000000000000000000 

[Observed]
bots = 000000000000000000 000000000000000000 000000000000000000
```

### Future plans
Revision of the code, because the development of the library "discord.py" ended on 28th August 2021...
Revision of the code with Nextcord, a fork of discord.py
