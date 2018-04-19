#!/usr/bin/python
from F1Calendar import F1Calendar
from DiscordWebhook import DiscordWebhook

DO_REQUEST = True
CALENDAR_FILE = "formula.1.2018.ics"
WEBHOOK_URL = open('webhook_url.conf', 'r').read().strip()

webhook = DiscordWebhook(WEBHOOK_URL)
cal = F1Calendar(CALENDAR_FILE)
next_event = cal.get_next_event()

if DO_REQUEST:
    webhook.send_message(next_event)
