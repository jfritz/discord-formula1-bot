#!/usr/bin/python
from DiscordWebhook import DiscordWebhook
from F1Calendar import F1Calendar

DO_REQUEST = False
CALENDAR_FILE = "formula.1.2018.ics"
WEBHOOK_URL = open('webhook_url.conf', 'r').read().strip()

webhook = DiscordWebhook(WEBHOOK_URL)
cal = F1Calendar(CALENDAR_FILE)

# todo if monday, do stuff
# todo if thurs-sat, do other stuff
events = cal.get_events()
events_str = "\n".join(events)

print "Next event: " + events_str

if DO_REQUEST:
    webhook.send_message(events_str)
