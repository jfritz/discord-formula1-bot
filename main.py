#!/usr/bin/python
import datetime
from DiscordWebhook import DiscordWebhook
from F1Calendar import F1Calendar

DO_REQUEST = True
CALENDAR_FILE = "formula.1.2018.ics"
WEBHOOK_URL = open('webhook_url.conf', 'r').readlines()[0].strip()

webhook = DiscordWebhook(WEBHOOK_URL)
cal = F1Calendar(CALENDAR_FILE)
dow = datetime.datetime.today().weekday()

# Monday
if dow == 0:
    prefix_str = u"Happy Monday! Here is the schedule for the next race weekend: \n"
    events = cal.get_next_race_events()
# Thurs, Fri, Sat
elif dow in (3, 4, 5):
    prefix_str = u"Race Weekend! In the next 24 hours: \n"
    events = cal.get_events_next_24h()


if events:
    events_str = "\n".join(events)
    print "Sending: " + prefix_str + events_str

    if DO_REQUEST:
        webhook.send_message(prefix_str + events_str)
