import datetime
from dateutil import tz
from icalendar import Calendar

class F1Calendar(object):

    # See https://pypi.org/project/icalendar/
    # See also https://icalendar.readthedocs.io/en/latest/usage.html
    def __init__(self, filename):
        self.filename = filename
        self.cal_data = Calendar.from_ical(open(self.filename, 'r').read())
        pass

    def get_next_event(self):
        return self.get_events()[0]

    def get_events(self, upcoming_only=True):
        ret = []

        for item in self.cal_data.walk():
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
                if upcoming_only and start < datetime.datetime.now().replace(tzinfo=tz.tzlocal()):
                    continue

                # calculate time difference from now
                # assumes times from calendar have a flat 0 microseconds set.
                # See https://stackoverflow.com/questions/3426870/calculating-time-difference#3427051
                now = datetime.datetime.now().replace(microsecond=0).replace(tzinfo=tz.tzlocal())
                diff = start_utc - now

                # Format string message for next event
                # See http://strftime.org/
                start_friendly = start.strftime("%a, %b %d %I:%M %p %Z")
                ret.append(u"**{}** starts in **{}** at **{}**".format(title, diff, start_friendly))

        return ret
