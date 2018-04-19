#!/usr/bin/python
import urllib2
import urllib
import datetime
from dateutil import tz
from icalendar import Calendar,vDatetime

DO_REQUEST = True
CALENDAR_FILE = "formula.1.2018.ics"
WEBHOOK_URL = open('webhook_url.conf','r').read().strip()
FORM_DATA = { 'content': 'Test Message! If you see this, the bot is broken!' }
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "DNT": "1",
    "Host":"discordapp.com",
    "Upgrade-Insecure-Requests":   "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
}


# read calendar file
# See https://pypi.org/project/icalendar/
# See also https://icalendar.readthedocs.io/en/latest/usage.html
cal_file = open(CALENDAR_FILE,'r')
cal_data = Calendar.from_ical(cal_file.read())

# read events in calendar
for item in cal_data.walk():
    if item.name == "VEVENT":

        # read event data
        title = item.get('summary').title()
        start_utc = item.get('dtstart').dt
        end_utc = item.get('dtend').dt
        
        # convert to local timezone
        # See https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime-with-python#4771733
        start = start_utc.astimezone(tz.tzlocal())
        end = end_utc.astimezone(tz.tzlocal())

        # Ignore past events
        if start < datetime.datetime.now().replace(tzinfo=tz.tzlocal()):
            continue

        # calculate time difference from now
        # assumes times from calendar have a flat 0 microseconds set.
        # See https://stackoverflow.com/questions/3426870/calculating-time-difference#3427051
        now = datetime.datetime.now().replace(microsecond=0).replace(tzinfo=tz.tzlocal())
        diff = start_utc - now

        # Format string message for next event
        # See http://strftime.org/
        start_friendly = start.strftime("%a, %b %d %I:%M %p %Z")
        FORM_DATA['content'] = u"**{}** starts in **{}** at **{}**".format(title, diff, start_friendly)
        print FORM_DATA['content']

        # Only print the next upcoming event.
        break

if DO_REQUEST:
    # Build request
    FORM_DATA = urllib.urlencode(FORM_DATA)
    api_request = urllib2.Request(url=WEBHOOK_URL,data=FORM_DATA,headers=HEADERS)

    print "Request:"
    print api_request

    # Send request, get response
    result = urllib2.urlopen(api_request)
    result_content = result.read()

    # See https://discordapp.com/developers/docs/topics/response-codes
    # for response code information.
    print """
    Result: {}
    Result Status: {}
    URL: {}
    Info: {}
    """.format(result_content, result.getcode(), result.geturl(), result.info())
