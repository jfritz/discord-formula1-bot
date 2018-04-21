import urllib
import urllib2


class DiscordWebhook(object):
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Host": "discordapp.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
    }

    def __init__(self, webhook_url, debug_mode=True):
        self.url = webhook_url
        self.debug = debug_mode

    def send_message(self, message):
        # Build request
        form_data = {'content': message}
        form_data = urllib.urlencode(form_data)
        api_request = urllib2.Request(url=self.url, data=form_data, headers=self.HEADERS)

        if self.debug:
            print "------------------------"
            print "Discord Webhook Request:"
            print api_request
            print "------------------------"

        # Send request, get response
        result = urllib2.urlopen(api_request)
        result_content = result.read()

        # See https://discordapp.com/developers/docs/topics/response-codes
        # for response code information.
        if self.debug:
            print "------------------------"
            print "Discord Webhook Response:"
            print """
{}
Result Status: {}
URL: {}
Info: {}
""".format(result_content, result.getcode(), result.geturl(), result.info())
            print "------------------------"

        return [result.getcode(), result.info()]
