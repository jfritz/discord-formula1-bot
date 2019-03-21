#!/usr/bin/python
import datetime
import os
from DiscordWebhook import DiscordWebhook
from F1Calendar import F1Calendar

DO_REQUEST = True
root_dir = os.path.dirname(os.path.realpath(__file__))
CALENDAR_FILE = root_dir + "/formula.1.2019.ics"
WEBHOOK_URL = open(root_dir + '/webhook_url.conf', 'r').readlines()[0].strip()

webhook = DiscordWebhook(WEBHOOK_URL)
cal = F1Calendar(CALENDAR_FILE)
dow = datetime.datetime.today().weekday()
output_str = None


dow = 0

# Monday
if dow == 0:
    prefix_str = u"<:f1:436383126743285760> Happy Monday! Here is the schedule for the next race weekend: \n"
    suffix_str = u"<:nico:436342726309445643>"
    events = cal.get_next_race_events()
    output_str = prefix_str + "\n".join(events) + suffix_str
# Thurs, Fri, Sat, Sun
elif dow in (3, 4, 5, 6):
    prefix_str = u"<:f1:436383126743285760> Race Weekend! In the next 24 hours: \n"
    suffix_str = u"<:nico:436342726309445643>"
    events = cal.get_events_next_24h()
    output_str = prefix_str + "\n".join(events) + suffix_str


if events:
    print "Sending: " + output_str.encode('utf-8')

    if DO_REQUEST:
        webhook.send_message(output_str)
